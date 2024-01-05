terraform {
  source = "${get_terragrunt_dir()}/../../../aws//route53-zone"
}

dependency "delegation-set" {
  config_path = "../route53-delegation-set-stonksfeed.com"
}

include {
  path = find_in_parent_folders()
}

inputs = {
  hosted_zone_domain_name = "stonksfeed.com"
  delegation_set_id = dependency.delegation-set.outputs.id
}
