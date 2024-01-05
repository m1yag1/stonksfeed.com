locals {
  domain_name = var.dns_domain
  subject_alternative_names = ["*.${local.domain_name}"]
  hosted_zone_id = var.hosted_zone_id
}

data "aws_route53_zone" "selected" {
  name = local.domain_name
}

resource "aws_acm_certificate" "default" {
  domain_name               = local.domain_name
  subject_alternative_names = local.subject_alternative_names
  validation_method         = "DNS"

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(
    {
      "ServiceName" = var.service_name
      "Environment" = var.env
    },
    var.extra_tags,
  )

}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.default.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = var.validation_record_ttl
  type            = each.value.type
  zone_id         = var.hosted_zone_id
}

resource "aws_acm_certificate_validation" "default" {
  certificate_arn = aws_acm_certificate.default.arn

  validation_record_fqdns = [for record in aws_route53_record.validation : record.fqdn]
}
