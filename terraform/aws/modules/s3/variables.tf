variable "bucket_name" {
  type = string
}

variable "force_destroy" {
  description = "Prevent the deletion of child folders or objects. Useful for development and not recommended for prod."
  default     = false
}
