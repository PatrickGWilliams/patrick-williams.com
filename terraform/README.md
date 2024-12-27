# Terraform Configuration for [patrick-williams.com](https://patrick-williams.com)

The `terraform` directory uses Terraform to create an AWS EC2 running an Ubuntu AMI with a local PostgreSQL back end. 

## PostgreSQL Setup
Before using Terraform, I start the PostgreSQL service:
```bash
systemctl start postgresql.service
```
Next, I define my database username and password as environment variables:
```bash
export PGUSER=username
read -s PGPASSWORD
export PGPASSWORD
```
Replacing username with my username and entering my password after I enter `read -s PGPASSWORD`.

## Running Terraform
After configuring the database credentials, I run the following commands to initialize Terraform and apply the configuration:
```bash
terraform init
terraform apply -var-file="secret.tfvars"
```
This creates the specified AWS resources using a variable file called `secret.tfvars` (Note: the variable file is not included in this repository).
