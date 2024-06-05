resource "aws_route53_record" "www" {
  zone_id = data.aws_route53_zone.pat_will.zone_id
  name    = data.aws_route53_zone.pat_will.name
  type    = "A"
  ttl     = 300
  records = [aws_eip.web_server_ip.public_ip]
}

data "aws_route53_zone" "pat_will" {
  name         = local.env.base_domain_name
}
