# Welcome to the repository for [patrick-williams.com](https://patrick-williams.com)!

### This is the repository for my personal website showcasing my skills, certifications, and sample python scripts. Below you'll find information about the project structure.
***
### The project is organized into several directories:

1. [Flask Directory](/../../tree/main/flask/): Contains the Python code, Jinja templates, CSS files, and Dockerfile I made to create the website. Additionally, it includes the Python code for my New York Times Letter Boxed puzzle helper ([Letter Box Helper](/../../blob/main/flask/PatrickWilliamsWebsite/app/lbHelper.py)).

2. [Terraform Directory](/../../tree/main/terraform/): Contains Terraform code to provision the website infrastructure. It utilizes a PostgreSQL back end to store the terraform state.

3. [Ansible Directory](/../../tree/main/ansible/): Contains Ansible code to configure the server, install relevant packages, start the Docker image, and obtain TLS certificates for the website.
