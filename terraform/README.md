# Terraform Configuration for [patrick-williams.com](https://patrick-williams.com)

This Terraform configuration creates an AWS EC2 running an Ubuntu ami using a local PostgreSQL back end. To use this Terraform first I start PostgreSQL:
```bash
systemctl start pastgrespl.service
```
Next I pass my Data Base username and password as environment variables like so:
```bash
export PGUSER=username
read -s PGPASSWORD
export PGPASSWORD
```
Replacing username with my username and entering my password after I enter `read -s PGPASSWORD`. Then I can run:
```bash
terraform init
terraform apply -var-file="secret.tfvars"
```
It then creates the specified AWS resources using a variable file called `secret.tfvars` (not included in this repository).
