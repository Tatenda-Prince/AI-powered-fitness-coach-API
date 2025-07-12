variable "aws_region" {
  default = "us-east-1"
}

variable "openai_api_key" {
  type      = string
  sensitive = true
}
