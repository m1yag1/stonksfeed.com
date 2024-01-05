variable "dns_domain" {
  description = "Domain to create cert for, e.g. example.com"
}

variable "hosted_zone_id" {
  description = "The hosted zone of the domain to create the valiation records"
}

variable "validation_record_ttl" {
  description = "Time-to-live for Route53 validation records"
  default     = 60
}

variable "extra_tags" {
  description = "Extra tags to attach to things"
  type        = map
  default     = {}
}
