terraform {
  source = "${get_terragrunt_dir()}/../../../aws/cloudfront"
}

include {
  path = find_in_parent_folders()
}

dependency "route53" {
  config_path = "../route53-zone-stonksfeed.com"
}

dependency "s3" {
  config_path = "../s3-stonksfeed.com"
}



inputs = {
  origin_bucket_arn = dependency.s3.outputs.arn
  origin_bucket_id = dependency.s3.outputs.id
  origin_bucket_domain_name = dependency.s3.outputs.bucket_regional_domain_name

  # Add alias for bare domain to distribution
  alias_domain = true
  create_dns = true

  # DNS zone
  dns_domain = dependency.route53.outputs.name
  dns_zone_id = dependency.route53.outputs.main_hosted_zone_id

}
