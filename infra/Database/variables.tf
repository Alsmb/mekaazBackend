variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "db_username" {
  type    = string
  default = "mekaaz"
}

variable "db_password" {
  type    = string
  description = "Use a secure password, or pass via terraform -var"
}
///SUPER_SECURE_PASS

variable "db_name" {
  type    = string
  default = "mekaazdb"
}