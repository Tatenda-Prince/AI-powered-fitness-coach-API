output "api_endpoint" {
  value = aws_apigatewayv2_api.api.api_endpoint
  description = "API Gateway endpoint URL"
}

output "website_url" {
  value = "https://${aws_cloudfront_distribution.website.domain_name}"
  description = "CloudFront website URL"
}

output "s3_bucket_name" {
  value = aws_s3_bucket.website.bucket
  description = "S3 bucket name for website files"
}

output "s3_website_url" {
  value = "http://${aws_s3_bucket_website_configuration.website.website_endpoint}"
  description = "S3 static website URL"
}
