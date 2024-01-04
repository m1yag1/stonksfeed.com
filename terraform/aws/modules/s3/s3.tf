resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name
  force_destroy = var.force_destroy

  tags = merge({
    Name = var.bucket_name
    Environment = var.env
    ServiceName = var.service_name
  }, var.extra_tags
  )
}
