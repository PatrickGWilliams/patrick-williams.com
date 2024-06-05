resource "aws_instance" "web_server" {
  ami               = "ami-0c7217cdde317cfec"
  instance_type     = local.env.web_server_instance_type
  availability_zone = local.env.availability_zone
  subnet_id         = aws_subnet.web_server.id
  key_name          = "key_name"
  vpc_security_group_ids = [
    aws_security_group.allow_http_https_internet.id,
    aws_security_group.allow_ssh_internet.id,
  ]

  tags = {
    Name = format("%s-server", local.env.app_name)
  }
}

resource "aws_eip_association" "web_server_eip_assoc" {
  instance_id   = aws_instance.web_server.id
  allocation_id = aws_eip.web_server_ip.id
}

resource "aws_eip" "web_server_ip" {
  tags = {
    Name = format("%s-ip", local.env.app_name)
  }
}

resource "aws_key_pair" "deployer" {
  key_name   = "key_name"
  public_key = file("/path/to/public_key")
}
