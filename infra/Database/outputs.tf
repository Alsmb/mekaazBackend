output "db_endpoint" {
  value = aws_db_instance.postgres.address
}

output "db_port" {
  value = aws_db_instance.postgres.port
}

//Run this once to create DB: cd infra/db && terraform init && terraform apply -var="db_password=YOUR_PASSWORD" -auto-approve