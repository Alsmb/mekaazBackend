data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "db_sg" {
  name   = "db-sg"
  vpc_id = data.aws_vpc.default.id

  # Allow Postgres from the VPC (app EC2 in same VPC can reach this)
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.default.cidr_block]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "postgres" {
  identifier              = "my-postgres-db"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  username                = var.db_username
  password                = var.db_password
  db_name                 = var.db_name
  vpc_security_group_ids  = [aws_security_group.db_sg.id]
  skip_final_snapshot     = false
  backup_retention_period = 7
  publicly_accessible     = false

  lifecycle {
    prevent_destroy = true
    ignore_changes  = [password]
  }
}
