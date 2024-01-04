variable "service_name" {
  description = "The name of the service"
}

variable "extra_tags" {
  description = "Extra tags to attach to things"
  type        = map
  default     = {}
}
