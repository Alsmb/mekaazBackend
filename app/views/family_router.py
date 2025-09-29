from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.family import (
    FamilyResponse, FamilyMemberResponse, FamilyInviteRequest, 
    FamilyJoinRequest, FamilySharingSettingsResponse, 
    FamilySharingSettingsUpdateRequest, FamilyMemberHealthResponse
)
from app.schemas.emergency import EmergencyContactCreateRequest, EmergencyContactResponse
from app.controllers.family_controller import FamilyController
from app.models.emergency_contact import EmergencyContact
import uuid
from datetime import datetime

router = APIRouter(prefix="/family", tags=["Family"])

@router.post("/create", response_model=FamilyResponse)
def create_family(
    data: FamilyInviteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new family and generate invite code"""
    family = FamilyController.create_family(db, str(current_user.id), data.family_name)
    return family

@router.post("/join", response_model=FamilyResponse)
def join_family(
    data: FamilyJoinRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Join a family using invite code"""
    family = FamilyController.join_family(db, str(current_user.id), data.invite_code)
    return family

@router.get("/members", response_model=list[FamilyMemberResponse])
def get_family_members(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all family members"""
    members = FamilyController.get_family_members(db, str(current_user.id))
    return members

@router.delete("/members/{member_id}")
def remove_family_member(
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a member from family (owner only)"""
    return FamilyController.remove_family_member(db, str(current_user.id), member_id)

@router.get("/members/{member_id}/health", response_model=FamilyMemberHealthResponse)
def get_member_health(
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health data for a family member (with sharing permissions)"""
    health_data = FamilyController.get_member_health(db, str(current_user.id), member_id)
    return health_data

@router.patch("/sharing-settings", response_model=FamilySharingSettingsResponse)
def update_sharing_settings(
    data: FamilySharingSettingsUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update family sharing settings"""
    # Get user's family ID
    from app.models.family import Family
    family = db.query(Family).filter_by(owner_id=str(current_user.id)).first()
    if not family:
        # Check if user is a member of another family
        from app.models.family import FamilyMember
        member = db.query(FamilyMember).filter_by(member_id=str(current_user.id)).first()
        if not member:
            raise HTTPException(status_code=404, detail="No family found")
        family = db.query(Family).filter_by(owner_id=member.owner_id).first()
    
    settings = FamilyController.update_sharing_settings(
        db, str(current_user.id), str(family.id), data.dict(exclude_unset=True)
    )
    return settings

# Emergency Contacts
@router.post("/emergency-contacts", response_model=EmergencyContactResponse)
def create_emergency_contact(
    data: EmergencyContactCreateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add emergency contact"""
    contact = EmergencyContact(
        id=str(uuid.uuid4()),
        user_id=str(current_user.id),
        name=data.name,
        phone=data.phone,
        relationship=data.relationship,
        is_primary=data.is_primary,
        created_at=datetime.utcnow()
    )
    
    # If this is primary, unset other primary contacts
    if data.is_primary:
        db.query(EmergencyContact).filter(
            EmergencyContact.user_id == str(current_user.id),
            EmergencyContact.is_primary == True
        ).update({"is_primary": False})
    
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact.to_dict()

@router.get("/emergency-contacts", response_model=list[EmergencyContactResponse])
def get_emergency_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all emergency contacts for user"""
    contacts = db.query(EmergencyContact).filter_by(user_id=str(current_user.id)).all()
    return [contact.to_dict() for contact in contacts]

@router.delete("/emergency-contacts/{contact_id}")
def delete_emergency_contact(
    contact_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete emergency contact"""
    contact = db.query(EmergencyContact).filter(
        EmergencyContact.id == contact_id,
        EmergencyContact.user_id == str(current_user.id)
    ).first()
    
    if not contact:
        raise HTTPException(status_code=404, detail="Emergency contact not found")
    
    db.delete(contact)
    db.commit()
    return {"message": "Emergency contact deleted successfully"} 

@router.get("/invite-code")
def get_family_invite_code(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get family invite code for sharing"""
    return FamilyController.get_family_invite_code(db, str(current_user.id))

@router.get("/pending-invites")
def get_pending_invites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get pending family invites for current user"""
    return FamilyController.get_pending_invites(db, str(current_user.id))

@router.post("/invites/{invite_id}/accept")
def accept_family_invite(
    invite_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Accept a family invite"""
    return FamilyController.accept_family_invite(db, str(current_user.id), invite_id)

@router.post("/invites/{invite_id}/reject")
def reject_family_invite(
    invite_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reject a family invite"""
    return FamilyController.reject_family_invite(db, str(current_user.id), invite_id)

@router.get("/members/{member_id}/health")
def get_family_member_health(
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health data for a family member"""
    return FamilyController.get_family_member_health(db, str(current_user.id), member_id)

@router.get("/health-summary")
def get_family_health_summary(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get health summary for all family members"""
    return FamilyController.get_family_health_summary(db, str(current_user.id)) 

@router.get("/health-dashboard")
def get_family_health_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive family health dashboard"""
    return FamilyController.get_family_health_dashboard(db, str(current_user.id))

@router.get("/health-comparison")
def get_family_health_comparison(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Compare health data across family members"""
    return FamilyController.get_family_health_comparison(db, str(current_user.id))

@router.post("/health-reports")
def generate_family_health_report(
    report_config: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate family health reports"""
    return FamilyController.generate_family_health_report(db, str(current_user.id), report_config)

@router.get("/members/{member_id}/detailed-health")
def get_family_member_detailed_health(
    member_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed health data for a family member"""
    return FamilyController.get_family_member_detailed_health(db, str(current_user.id), member_id) 