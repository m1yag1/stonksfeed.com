locals {
  cert_domain = replace(var.dns_domain, "/\\.$/", "") # zone_name has trailing dot, but cert does not
  fqdn        = local.cert_domain
  aliases     = [local.fqdn]
  has_cert    = var.enable_acm_cert
}

data "aws_caller_identity" "current" {
}

provider "aws" {
  alias  = "cloudfront"
  region = "us-east-1"
}

# Certificate managed by ACM
data "aws_acm_certificate" "host_acm" {
  count    = var.enable_acm_cert ? 1 : 0
  provider = aws.cloudfront
  domain   = local.cert_domain
  statuses = ["ISSUED"]
}

resource "aws_cloudfront_origin_access_identity" "main" {
  comment = "${var.service_name}-${var.env}"
}

# Give CloudFront access to bucket where assets are stored
data "aws_iam_policy_document" "cloudfront" {
  statement {
    actions   = ["s3:ListBucket"]
    resources = [var.origin_bucket_arn]
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.main.iam_arn]
    }
  }

  statement {
    actions   = ["s3:GetObject"]
    resources = ["${var.origin_bucket_arn}/*"]
    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.main.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "origin_bucket_policy" {
  bucket = var.origin_bucket_id
  policy = data.aws_iam_policy_document.cloudfront.json
}

# https://www.terraform.io/docs/providers/aws/r/cloudfront_distribution.html
# https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_UpdateDistribution.html
resource "aws_cloudfront_distribution" "main" {
  enabled         = true
  is_ipv6_enabled = true
  price_class     = var.price_class

  default_root_object = "index.html"
  comment             = "${var.service_name} ${var.env}"
  aliases = local.aliases


  origin {
    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.main.cloudfront_access_identity_path
    }
    origin_path = var.origin_path

    domain_name = var.origin_bucket_domain_name
    origin_id   = var.origin_bucket_id
  }

  dynamic "viewer_certificate" {
    for_each = var.enable_acm_cert ? tolist([1]) : []

    content {
      acm_certificate_arn      = data.aws_acm_certificate.host_acm[0].arn
      ssl_support_method       = "sni-only"
      minimum_protocol_version = "TLSv1"
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  default_cache_behavior {
    # allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.origin_bucket_id

    forwarded_values {
      query_string = true

      cookies {
        forward = "none"
      }
    }

    dynamic "lambda_function_association" {
      for_each = var.lambda_arn == null ? [] : tolist([1])
      content {
        event_type = "origin-request"
        lambda_arn = var.lambda_arn
        # include_body = false
      }
    }

    viewer_protocol_policy = var.viewer_protocol_policy
    min_ttl                = var.min_ttl
    default_ttl            = var.default_ttl
    max_ttl                = var.max_ttl
    compress               = var.compress
  }

  tags = merge(
    {
      "Name" = local.fqdn
      "Application" = var.service_name
      "Environment"   = var.env
    },
    var.extra_tags,
  )
}

# https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resource-record-sets-values-alias.html
resource "aws_route53_record" "main" {
  count = var.create_dns ? 1 : 0

  zone_id = var.dns_zone_id
  name    = local.cert_domain
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = true
  }
}

resource "aws_route53_record" "main-aaaa" {
  count = var.create_dns ? 1 : 0

  zone_id = var.dns_zone_id
  name    = local.cert_domain
  type    = "AAAA"

  alias {
    name                   = aws_cloudfront_distribution.main.domain_name
    zone_id                = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health = true
  }
}
