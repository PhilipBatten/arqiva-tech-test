# ECR Repository
resource "aws_ecr_repository" "lambda_container" {
  name = "lambda-container"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}
