terraform {
  source = "${get_terragrunt_dir()}/../../../aws/acm-public"
}

include {
  path = find_in_parent_folders()
}

dependency "route53-public" {
  config_path = "../route53-zone-stonksfeed.com"
}

inputs = {
    dns_domain = dependency.route53-public.outputs.name_nodot
    hosted_zone_id = dependency.route53-public.outputs.main_hosted_zone_id
}
