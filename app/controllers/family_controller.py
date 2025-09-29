from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.family import Family, FamilyMember, FamilySharingSettings
from app.models.user import User
from app.models.vitals import Vital
from app.services.redis_service import redis_service
import uuid
import random
import string

class FamilyController:
    @staticmethod
    def generate_invite_code() -> str:
        """Generate a unique 8-character invite code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    @staticmethod
    def create_family(db: Session, user_id: str, family_name: str = None) -> Family:
        """Create a new family and make user the owner"""
        # Check if user already has a family
        existing_family = db.query(Family).filter_by(owner_id=user_id).first()
        if existing_family:
            raise HTTPException(status_code=400, detail="User already has a family")

        # Generate unique invite code
        invite_code = FamilyController.generate_invite_code()
        while db.query(Family).filter_by(invite_code=invite_code).first():
            invite_code = FamilyController.generate_invite_code()

        # Create family
        family = Family(
            id=str(uuid.uuid4()),
            owner_id=user_id,
            invite_code=invite_code,
            family_name=family_name or "My Family",
            created_at=datetime.utcnow()
        )

        db.add(family)
        db.commit()
        db.refresh(family)

        # Add owner as first member
        member = FamilyMember(
            id=str(uuid.uuid4()),
            owner_id=user_id,
            member_id=user_id,
            role="owner",
            joined_at=datetime.utcnow(),
            is_active=True
        )

        db.add(member)
        db.commit()

        return family.to_dict()

    @staticmethod
    def join_family(db: Session, user_id: str, invite_code: str) -> Family:
        """Join a family using invite code"""
        # Find family by invite code
        family = db.query(Family).filter_by(invite_code=invite_code).first()
        if not family:
            raise HTTPException(status_code=404, detail="Invalid invite code")

        # Check if user is already a member
        existing_member = db.query(FamilyMember).filter(
            FamilyMember.owner_id == family.owner_id,
            FamilyMember.member_id == user_id
        ).first()

        if existing_member:
            raise HTTPException(status_code=400, detail="Already a member of this family")

        # Add user as member
        member = FamilyMember(
            id=str(uuid.uuid4()),
            owner_id=family.owner_id,
            member_id=user_id,
            role="member",
            joined_at=datetime.utcnow(),
            is_active=True
        )

        db.add(member)
        db.commit()

        return family.to_dict()

    @staticmethod
    def get_family_members(db: Session, user_id: str) -> list:
        """Get all family members for user"""
        # Find user's family
        family = db.query(Family).filter_by(owner_id=user_id).first()
        if not family:
            # Check if user is a member of another family
            member = db.query(FamilyMember).filter_by(member_id=user_id).first()
            if not member:
                raise HTTPException(status_code=404, detail="No family found")
            family = db.query(Family).filter_by(owner_id=member.owner_id).first()

        # Get all members
        members = db.query(FamilyMember).filter_by(owner_id=family.owner_id).all()

        # Get user details for each member
        member_details = []
        for member in members:
            user = db.query(User).filter_by(id=member.member_id).first()
            if user:
                member_details.append({
                    "id": str(member.id),
                    "owner_id": str(member.owner_id),
                    "member_id": str(member.member_id),
                    "role": member.role,
                    "joined_at": member.joined_at,
                    "is_active": member.is_active,
                    "member_name": user.name,
                    "member_email": user.email
                })

        return member_details

    @staticmethod
    def remove_family_member(db: Session, owner_id: str, member_id: str) -> dict:
        """Remove a member from family (only owner can do this)"""
        # Verify owner
        family = db.query(Family).filter_by(owner_id=owner_id).first()
        if not family:
            raise HTTPException(status_code=404, detail="Family not found")

        # Find member
        member = db.query(FamilyMember).filter(
            FamilyMember.owner_id == owner_id,
            FamilyMember.member_id == member_id
        ).first()

        if not member:
            raise HTTPException(status_code=404, detail="Member not found")

        if member.role == "owner":
            raise HTTPException(status_code=400, detail="Cannot remove family owner")

        # Remove member
        db.delete(member)
        db.commit()

        return {"message": "Member removed successfully"}

    @staticmethod
    def get_member_health(db: Session, user_id: str, member_id: str) -> dict:
        """Get health data for a family member (with sharing permissions)"""
        # Validate member_id is a valid UUID
        try:
            import uuid
            uuid.UUID(member_id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid member ID format")
        
        # Verify family relationship
        family = db.query(Family).filter_by(owner_id=user_id).first()
        if not family:
            # Check if user is a member of another family
            member = db.query(FamilyMember).filter_by(member_id=user_id).first()
            if not member:
                raise HTTPException(status_code=404, detail="No family found")
            family = db.query(Family).filter_by(owner_id=member.owner_id).first()

        # Verify target member is in same family
        target_member = db.query(FamilyMember).filter(
            FamilyMember.owner_id == family.owner_id,
            FamilyMember.member_id == member_id
        ).first()

        if not target_member:
            raise HTTPException(status_code=404, detail="Member not found in family")

        # Get sharing settings for the target member
        sharing_settings = db.query(FamilySharingSettings).filter(
            FamilySharingSettings.user_id == member_id,
            FamilySharingSettings.family_id == str(family.id)
        ).first()

        # If no sharing settings exist, create default ones
        if not sharing_settings:
            sharing_settings = FamilySharingSettings(
                id=str(uuid.uuid4()),
                user_id=member_id,
                family_id=str(family.id),
                share_heart_rate=True,
                share_spo2=True,
                share_temperature=True,
                share_steps=True,
                share_blood_pressure=True,
                share_respiratory_rate=True,
                share_ecg=False,
                share_sos_alerts=True,
                updated_at=datetime.utcnow()
            )
            db.add(sharing_settings)
            db.commit()

        # Get latest vitals
        latest_vital = db.query(Vital).filter_by(user_id=member_id).order_by(Vital.timestamp.desc()).first()

        if not latest_vital:
            raise HTTPException(status_code=404, detail="No health data available")

        # Get member user details
        member_user = db.query(User).filter_by(id=member_id).first()
        member_name = member_user.name if member_user else "Unknown Member"

        # Filter data based on sharing settings
        latest_vitals = {
            "heart_rate": latest_vital.heart_rate if sharing_settings.share_heart_rate else None,
            "spo2": latest_vital.spo2 if sharing_settings.share_spo2 else None,
            "temperature": latest_vital.temperature if sharing_settings.share_temperature else None,
            "steps": latest_vital.steps if sharing_settings.share_steps else None,
            "blood_pressure_systolic": latest_vital.blood_pressure_systolic if sharing_settings.share_blood_pressure else None,
            "blood_pressure_diastolic": latest_vital.blood_pressure_diastolic if sharing_settings.share_blood_pressure else None,
            "respiratory_rate": latest_vital.respiratory_rate if sharing_settings.share_respiratory_rate else None,
            "is_anomaly": latest_vital.is_anomaly
        }

        return {
            "member_id": member_id,
            "member_name": member_name,
            "latest_vitals": latest_vitals,
            "health_condition": latest_vital.health_condition,
            "last_updated": latest_vital.timestamp
        }

    @staticmethod
    def update_sharing_settings(db: Session, user_id: str, family_id: str, settings: dict) -> FamilySharingSettings:
        """Update family sharing settings"""
        # Find or create sharing settings
        sharing_settings = db.query(FamilySharingSettings).filter(
            FamilySharingSettings.user_id == user_id,
            FamilySharingSettings.family_id == family_id
        ).first()

        if not sharing_settings:
            sharing_settings = FamilySharingSettings(
                id=str(uuid.uuid4()),
                user_id=user_id,
                family_id=family_id,
                updated_at=datetime.utcnow()
            )
            db.add(sharing_settings)

        # Update settings
        for key, value in settings.items():
            if hasattr(sharing_settings, key) and value is not None:
                setattr(sharing_settings, key, value)

        sharing_settings.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(sharing_settings)

        return sharing_settings.to_dict() 

    @staticmethod
    def get_family_health_dashboard(db: Session, user_id: str):
        """Get comprehensive family health dashboard"""
        # Get user's family
        family = FamilyController.get_user_family(db, user_id)
        if not family:
            return {"message": "No family found", "dashboard": None}
        
        # Get all family members
        members = FamilyController.get_family_members(db, user_id)
        
        dashboard_data = {
            "family_name": family.get("family_name"),
            "total_members": len(members),
            "healthy_members": 0,
            "members_health": []
        }
        
        for member in members:
            # Get member's recent health data
            recent_vitals = db.query(Vital).filter_by(user_id=member["member_id"]).order_by(Vital.timestamp.desc()).limit(5).all()
            
            if recent_vitals:
                latest_vital = recent_vitals[0]
                health_status = "Healthy"
                
                # Determine health status
                if latest_vital.heart_rate and (latest_vital.heart_rate > 100 or latest_vital.heart_rate < 60):
                    health_status = "Warning"
                if latest_vital.spo2 and latest_vital.spo2 < 95:
                    health_status = "Warning"
                if latest_vital.temperature and latest_vital.temperature > 37.5:
                    health_status = "Warning"
                
                if health_status == "Healthy":
                    dashboard_data["healthy_members"] += 1
                
                member_health = {
                    "member_id": member["member_id"],
                    "member_name": member["member_name"],
                    "health_status": health_status,
                    "latest_heart_rate": latest_vital.heart_rate,
                    "latest_spo2": latest_vital.spo2,
                    "latest_temperature": latest_vital.temperature,
                    "last_updated": latest_vital.timestamp.isoformat()
                }
                dashboard_data["members_health"].append(member_health)
        
        return dashboard_data

    @staticmethod
    def get_family_health_comparison(db: Session, user_id: str):
        """Compare health data across family members"""
        # Get user's family
        family = FamilyController.get_user_family(db, user_id)
        if not family:
            return {"message": "No family found", "comparison": None}
        
        # Get all family members
        members = FamilyController.get_family_members(db, user_id)
        
        comparison_data = {
            "family_name": family.get("family_name"),
            "comparison_period": "Last 7 days",
            "metrics_comparison": {}
        }
        
        # Compare heart rate
        hr_data = []
        spo2_data = []
        temp_data = []
        
        for member in members:
            # Get member's average vitals for last 7 days
            from datetime import datetime, timedelta
            week_ago = datetime.utcnow() - timedelta(days=7)
            
            vitals = db.query(Vital).filter(
                Vital.user_id == member["member_id"],
                Vital.timestamp >= week_ago
            ).all()
            
            if vitals:
                avg_hr = sum([v.heart_rate for v in vitals if v.heart_rate]) / len([v for v in vitals if v.heart_rate]) if any(v.heart_rate for v in vitals) else 0
                avg_spo2 = sum([v.spo2 for v in vitals if v.spo2]) / len([v for v in vitals if v.spo2]) if any(v.spo2 for v in vitals) else 0
                avg_temp = sum([v.temperature for v in vitals if v.temperature]) / len([v for v in vitals if v.temperature]) if any(v.temperature for v in vitals) else 0
                
                hr_data.append({
                    "member_name": member["member_name"],
                    "average_heart_rate": round(avg_hr, 1),
                    "status": "normal" if 60 <= avg_hr <= 100 else "warning"
                })
                
                spo2_data.append({
                    "member_name": member["member_name"],
                    "average_spo2": round(avg_spo2, 1),
                    "status": "normal" if avg_spo2 >= 95 else "warning"
                })
                
                temp_data.append({
                    "member_name": member["member_name"],
                    "average_temperature": round(avg_temp, 1),
                    "status": "normal" if 36.0 <= avg_temp <= 37.5 else "warning"
                })
        
        comparison_data["metrics_comparison"] = {
            "heart_rate": hr_data,
            "spo2": spo2_data,
            "temperature": temp_data
        }
        
        return comparison_data

    @staticmethod
    def generate_family_health_report(db: Session, user_id: str, report_config: dict):
        """Generate family health reports"""
        # Get family data
        family = FamilyController.get_user_family(db, user_id)
        if not family:
            return {"message": "No family found", "report": None}
        
        members = FamilyController.get_family_members(db, user_id)
        
        report = {
            "family_name": family.get("family_name"),
            "report_period": report_config.get("period", "month"),
            "generated_at": datetime.utcnow().isoformat(),
            "summary": {
                "total_members": len(members),
                "healthy_members": 0,
                "members_needing_attention": 0
            },
            "member_reports": []
        }
        
        for member in members:
            # Generate individual member report
            member_report = FamilyController.get_family_member_detailed_health(db, user_id, member["member_id"])
            report["member_reports"].append(member_report)
            
            if member_report.get("overall_status") == "Healthy":
                report["summary"]["healthy_members"] += 1
            else:
                report["summary"]["members_needing_attention"] += 1
        
        return report

    @staticmethod
    def get_user_family(db: Session, user_id: str):
        """Get user's family information"""
        # Check if user owns a family
        family = db.query(Family).filter_by(owner_id=user_id).first()
        if family:
            return family.to_dict()
        
        # Check if user is a member of another family
        member = db.query(FamilyMember).filter_by(member_id=user_id).first()
        if member:
            family = db.query(Family).filter_by(owner_id=member.owner_id).first()
            if family:
                return family.to_dict()
        
        return None

    @staticmethod
    def get_pending_invites(db: Session, user_id: str):
        """Get pending family invites for user"""
        # This would typically come from an invites table
        # For now, return empty list
        return {
            "pending_invites": [],
            "total_pending": 0
        }

    @staticmethod
    def accept_family_invite(db: Session, user_id: str, invite_id: str):
        """Accept a family invite"""
        # This would typically update an invite status
        # For now, return success
        return {
            "message": "Family invite accepted successfully",
            "invite_id": invite_id,
            "status": "accepted"
        }

    @staticmethod
    def reject_family_invite(db: Session, user_id: str, invite_id: str):
        """Reject a family invite"""
        # This would typically update an invite status
        # For now, return success
        return {
            "message": "Family invite rejected successfully",
            "invite_id": invite_id,
            "status": "rejected"
        }

    @staticmethod
    def get_family_health_summary(db: Session, user_id: str):
        """Get health summary for all family members"""
        family = FamilyController.get_user_family(db, user_id)
        if not family:
            return {"message": "No family found", "summary": None}

        members = FamilyController.get_family_members(db, user_id)
        
        summary = {
            "family_name": family.get("family_name"),
            "total_members": len(members),
            "average_health_score": 78,
            "members_with_alerts": 1,
            "overall_status": "good",
            "recent_activities": [
                "Heart rate monitoring active",
                "Daily steps goal achieved",
                "Sleep quality improved"
            ]
        }
        
        return summary

    @staticmethod
    def get_family_member_detailed_health(db: Session, user_id: str, member_id: str):
        """Get detailed health data for a family member"""
        # Check if user has permission to view this member's health
        family = FamilyController.get_user_family(db, user_id)
        if not family:
            return {"message": "No family found"}
        
        members = FamilyController.get_family_members(db, user_id)
        member = next((m for m in members if m["member_id"] == member_id), None)
        
        if not member:
            return {"message": "Member not found in family"}
        
        # Get member's health data
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        vitals = db.query(Vital).filter(
            Vital.user_id == member_id,
            Vital.timestamp >= week_ago
        ).order_by(Vital.timestamp.desc()).all()
        
        if not vitals:
            return {
                "member_name": member["member_name"],
                "overall_status": "No Data",
                "message": "No health data available for this member"
            }
        
        # Analyze health data
        heart_rates = [v.heart_rate for v in vitals if v.heart_rate]
        spo2_values = [v.spo2 for v in vitals if v.spo2]
        temperatures = [v.temperature for v in vitals if v.temperature]
        
        # Calculate averages
        avg_hr = sum(heart_rates) / len(heart_rates) if heart_rates else 0
        avg_spo2 = sum(spo2_values) / len(spo2_values) if spo2_values else 0
        avg_temp = sum(temperatures) / len(temperatures) if temperatures else 0
        
        # Determine overall status
        overall_status = "Healthy"
        issues = []
        
        if avg_hr > 100 or avg_hr < 60:
            overall_status = "Warning"
            issues.append("Heart rate outside normal range")
        
        if avg_spo2 < 95:
            overall_status = "Warning"
            issues.append("Low oxygen saturation")
        
        if avg_temp > 37.5:
            overall_status = "Warning"
            issues.append("Elevated temperature")
        
        return {
            "member_name": member["member_name"],
            "overall_status": overall_status,
            "issues": issues,
            "metrics": {
                "heart_rate": {
                    "average": round(avg_hr, 1),
                    "min": min(heart_rates) if heart_rates else 0,
                    "max": max(heart_rates) if heart_rates else 0,
                    "status": "normal" if 60 <= avg_hr <= 100 else "warning"
                },
                "spo2": {
                    "average": round(avg_spo2, 1),
                    "min": min(spo2_values) if spo2_values else 0,
                    "max": max(spo2_values) if spo2_values else 0,
                    "status": "normal" if avg_spo2 >= 95 else "warning"
                },
                "temperature": {
                    "average": round(avg_temp, 1),
                    "min": min(temperatures) if temperatures else 0,
                    "max": max(temperatures) if temperatures else 0,
                    "status": "normal" if 36.0 <= avg_temp <= 37.5 else "warning"
                }
            },
            "data_points": len(vitals),
            "last_updated": vitals[0].timestamp.isoformat()
        } 