data "aws_vpc" "default" {
  default = true
}

resource "aws_subnet" "web_server" {
  vpc_id = data.aws_vpc.default.id

  cidr_block        = local.env.cidr_block
  availability_zone = local.env.availability_zone

  tags = {
    Name = format("%s-subnet", local.env.app_name)
  }
}

