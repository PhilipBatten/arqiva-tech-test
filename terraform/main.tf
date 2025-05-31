# DynamoDB Table
resource "aws_dynamodb_table" "app_table" {
  name           = "app-table"
  billing_mode   = "PROVISIONED"  # Changed to PROVISIONED for free tier
  read_capacity  = 5              # Free tier includes 25 RCU
  write_capacity = 5              # Free tier includes 25 WCU
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Environment = "production"
  }
}

# Lambda Function
resource "aws_lambda_function" "app_lambda" {
  function_name = "app-lambda"
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.lambda_container.repository_url}:latest"
  role          = aws_iam_role.lambda_role.arn
  timeout       = 30
  memory_size   = 128  # Reduced to 128MB to stay within free tier more easily

  depends_on = [
    aws_iam_role.lambda_role,
    aws_ecr_repository.lambda_container
  ]

  environment {
    variables = {
      DYNAMODB_TABLE = aws_dynamodb_table.app_table.name
    }
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Lambda to access DynamoDB
resource "aws_iam_role_policy" "lambda_dynamodb_policy" {
  name = "lambda_dynamodb_policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Scan",
          "dynamodb:Query"
        ]
        Resource = aws_dynamodb_table.app_table.arn
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# REST API Gateway (changed from HTTP API to REST API for free tier)
resource "aws_api_gateway_rest_api" "lambda_api" {
  name = "lambda-api"
}

# API Gateway Resource
resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.lambda_api.id
  parent_id   = aws_api_gateway_rest_api.lambda_api.root_resource_id
  path_part   = "{proxy+}"
}

# API Gateway Method
resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.lambda_api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

# API Gateway Integration
resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id = aws_api_gateway_rest_api.lambda_api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.proxy.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.app_lambda.invoke_arn
}

# API Gateway Deployment
resource "aws_api_gateway_deployment" "lambda_deployment" {
  rest_api_id = aws_api_gateway_rest_api.lambda_api.id

  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
}

# API Gateway Stage
resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.lambda_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.lambda_api.id
  stage_name    = "prod"
}

# Lambda Permission for API Gateway
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.app_lambda.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.lambda_api.execution_arn}/*/*"
}

# Add IAM policy for Lambda to pull from ECR
resource "aws_iam_role_policy" "lambda_ecr_pull" {
  name = "lambda_ecr_pull"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ecr:GetDownloadUrlForLayer",
          "ecr:BatchGetImage"
        ]
        Resource = aws_ecr_repository.lambda_container.arn
      }
    ]
  })
}

# Output the API Gateway URL
output "api_url" {
  value = "${aws_api_gateway_stage.prod.invoke_url}/{proxy}"
  description = "API Gateway URL"
} 