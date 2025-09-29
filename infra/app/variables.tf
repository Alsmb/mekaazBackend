variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "instance_type" {
  type    = string
  default = "t2.micro"
}

variable "key_name" {
  type = string
  default = "private-key"
}

variable "allowed_ip" {
  type    = string
  description = "Your public IP/32 for SSH"
    default = "188.48.161.243/32"
}