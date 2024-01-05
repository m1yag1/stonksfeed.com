resource "aws_route53_zone" "main" {
  name = var.hosted_zone_domain_name
  delegation_set_id = var.delegation_set_id
  force_destroy = var.force_destroy
}
