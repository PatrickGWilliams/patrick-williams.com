# Welcome to the repository for [patrick-williams.com](https://patrick-williams.com)!

### This is the repository for my personal website showcasing my skills, certifications, and sample python scripts. Below you'll find information about the project structure.
***
### The project is organized into several directories:

1. [Flask Directory](/../../tree/main/flask/): Contains the Python code, Jinja templates, and CSS files I made to create the website. Additionally, it includes the Python code for my New York Times Letter Boxed puzzle helper ([Spelling Bee Solver](/../../blob/main/flask/PatrickWilliamsWebsite/app/lbHelper.py)).

2. [Docker Directory](/../../tree/main/docker/): Contains the Dockerfile I used to build an image of the website.

3. [Terraform Directory](/../../tree/main/terraform/): Contains Terraform code to provision the website infrastructure. It utilizes a PostgreSQL back end to store the terraform state.

4. [Ansible Directory](/../../tree/main/ansible/): Contains Ansible code to configure the server, install relevant packages, start the Docker image, and obtain TLS certificates for the website. It also includes a Python script that uses Selenium to check which words the New York Times Spelling Bee puzzle will accept for that day. It is located [here](/../../blob/main/ansible/roles/patsite/files/app_files/NYTTester.py).
