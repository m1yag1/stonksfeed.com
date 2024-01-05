variable "hosted_zone_domain_name" {
  type = string
}


variable "delegation_set_id" {
  description = "The id of the delegation set"
  type = string
}

variable "force_destroy" {
  description = "Force destroy even if there are subdomains"
  default     = false
}
