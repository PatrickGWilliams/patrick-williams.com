# Ansible configuration for [patrick-williams.com](https://patrick-williams.com).

The `ansible` directory uses Ansible to initialize and configure the server to run my website.

## Initialization
1. I add the domain name (`patrick-williams.com`) to the inventory file under the `initialize` group
2. I then run the following command to initialize the server:
```bash
ansible-playbook --private-key /path/to/private/key initialize.yml
```
This Ansible playbook runs the `common` role in the `roles` directory. This role does the following:

1. Sets the host name  
2. Configures the admin users (defined in `group_vars/all.yml`) with password-less sudo using key files

## Website Configuration
Once initialized, I move the domain name in the inventory to the `website` group and run:
```bash
ansible-playbook --private-key /path/to/private/key -J site.yml
```
This playbook runs the `patsite` role on the `website` group. It performs the following steps: 

1. Prompts for the password to the Ansible Vault file, which contains the credentials to my Dockerhub account (Note: The vault file is not included in this repository)
2. The `patsite` role runs its dependencies starting with the `docker` role

### Docker Role

The `docker` role does the following:

1. Downloads and installs Docker 
2. Creates a docker group
3. Adds the ansible user to the docker group 

### Nginx Role

Next, The `Nginx` role: 

1. Installs Nginx 
2. Creates a directory to store Nginx logs
3. Ensures Nginx is running 

### Patsite Role

Finally, the `patsite` role: 

1. Removes the AWS created ubuntu user
2. Ensures the scraper script runs every day at 3:05
3. Copies the SQLite database file over to EC2 instance if it does not already exist there
4. Checks if docker is running the current version of the website image. If not, runs the `container_setup.yml` playbook
5. Ensures Nginx is running

### Container Setup

If the `container_setup.yml` playbook is ran it performs the following:

1. Logs into docker hub  
3. Downloads and starts the website image, exposing it on port 8024 on the EC2 instance. 
3. Logs out of docker hub 

### Optional SSL Role:

There is also an optional `ssl` role that uses `acme.sh` to enable HTTPS for my website.

Now the website can be accessed from [https://patrick-williams.com](https://patrick-williams.com). 
