# Ansible configuration for [patrick-williams.com](https://patrick-williams.com).

This directory uses Ansible to initialize and configure the server to run my website. It also includes a Python script that runs daily, using Selenium to check which words the New York Times Spelling Bee puzzle will accept for that day. It is located [here](/../../blob/main/ansible/roles/patsite/files/wordChecker/NYTTester.py). First I put the domain name (patrick-williams.com) in the inventory file in the 
initialize group. I then run:
```bash
ansible-playbook --private-key /path/to/private/key initailize.yml
```
This Ansible playbook runs the common role in the roles directory. This roles does the following:
1. Sets the host name  
2. Configures the admin users in group_vars/all.yml with password-less sudo using key files contained in the directory roles/common/files ( not included in this repository). 
Once initialized, I move the domain name in the inventory to the website group. Then run:
```bash
ansible-playbook --private-key /path/to/private/key --vault-id @prompt site.yml
```
This playbook runs the patsite role on the website group. 
1. First this command prompts for the password to the Ansible vault file containing the password and username to my Dockerhub account(not included in this repository). 
2. Then, the patsite role runs its dependencies starting with the docker role.

The docker role does the following:

1. Downloads and installs docker 
2. Creates a docker group. 
3. Adds the ansible user to the docker group 

Next, The Nginx role: 

1. Installs Nginx 
2. Creates a directory to store Nginx logs
3. Ensures Nginx is running 

The last dependency is the NYTTester_setup role:

1. Installs Python and Pip
2. Uses pip to install Selenium
3. Sets up a cron job to run the NYTTester.py every day at 3:05 a.m. just after the New York Times has updated the spelling bee puzzle for that day
4. Copies the NYTTester.py script to the server

Finally, the patsite role is ran. This role: 

1. Removes the aws created ubuntu user
2. Copies the SQLite database file and the word list file over to EC2 if they do not already exist there.
3. Checks if docker is running the current version of the website image and if not runs the container_setup.yml playbook
4. Ensures Nginx is running. 

If the container_setup.yml playbook is ran it:

1. Logs into docker hub  
3. Downloads and starts the image, exposing it on port 8024 on the Ubuntu server. 
3. Finally it logs out of docker hub 

There is also an optional ssl role that uses acme.sh to enable HTTPS for my website.

Now the website can be accessed from [https://patrick-williams.com](https://patrick-williams.com). 

