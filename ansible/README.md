# Ansible configuration for [patrick-williams.com](https://patrick-williams.com).

This directory uses Ansible to initialize and configure the server to run my website. First I put the domain name (patrick-williams.com) in the inventory file in the 
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

Finally, the patsite role is ran. This role: 

1. Removes the aws created ubuntu user
2. Ensures the scraper script runs every day at 3:05.
3. Copies the SQLite database file over to EC2 if it does not already exist there.
4. Checks if docker is running the current version of the website image and if not runs the container_setup.yml playbook
5. Ensures Nginx is running. 

If the container_setup.yml playbook is ran it:

1. Logs into docker hub  
3. Downloads and starts the image, exposing it on port 8024 on the Ubuntu server. 
3. Finally it logs out of docker hub 

There is also an optional ssl role that uses acme.sh to enable HTTPS for my website.

Now the website can be accessed from [https://patrick-williams.com](https://patrick-williams.com). 

