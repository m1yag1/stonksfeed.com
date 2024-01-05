output "main_hosted_zone_id" {
    value = aws_route53_zone.main.zone_id
    description = "The ID of the main hosted zone"
}
output "name" {
  description = "The Hosted Zone name"
  value       = aws_route53_zone.main.name
}

output "name_nodot" {
  description = "The Hosted Zone name without the trailing dot"
  value       = replace(aws_route53_zone.main.name, "/\\.$/", "")
}
