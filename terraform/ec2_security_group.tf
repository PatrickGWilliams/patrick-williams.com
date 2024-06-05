resource "aws_security_group" "allow_http_https_internet" {
  name        = format("%s-allow_http_https_internet", local.env.app_name)
  description = "Allow http and https inbound traffic from Internet"

  ingress {
    description = "https from Internet"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "http from internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = format("%s-allow_http_https_internet", local.env.app_name)
  }
}

resource "aws_security_group" "allow_ssh_internet" {
  name        = format("%s-allow_ssh_interent", local.env.app_name)
  description = "Allow ssh inbound traffic from Internet"

  ingress {
    description = "ssh from Internet"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = format("%s-allow_ssh_interent", local.env.app_name)
  }
}

