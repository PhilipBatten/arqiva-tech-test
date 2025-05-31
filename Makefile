.PHONY: run stop clean provision-ecr deploy-image provision-infra

# Variables
VALUE ?= dynamic string
AWS_REGION ?= eu-west-2
ECR_REPO ?= lambda-container

help:
	@echo "Available commands:"
	@echo "  make run            - Start the application"
	@echo "  make stop           - Stop all containers"
	@echo "  make clean          - Remove all containers and volumes"
	@echo "  make provision-ecr  - Provision ECR repository using Terraform"
	@echo "  make deploy-image   - Build and deploy container image to ECR"
	@echo "  make provision-infra - Provision all infrastructure except ECR"

run:
	@echo "Building and starting application and LocalStack..."
	docker compose build
	docker compose up -d
	@echo "Waiting for services to be ready..."
	sleep 5
	@echo "Initializing dynamodb table..."
	docker compose exec app python setup_localstack.py

stop:
	@echo "Stopping services..."
	docker compose down

clean: stop
	@echo "Cleaning up..."
	docker compose down -v
	rm -rf ./volume

deploy: provision-ecr deploy-image provision-infra

provision-ecr:
	@echo "Provisioning ECR repository..."
	cd terraform && terraform init && terraform apply -target=aws_ecr_repository.lambda_container -auto-approve
	@echo "ECR repository provisioned successfully!"

deploy-image:
	./deploy.sh

provision-infra:
	@echo "Provisioning infrastructure..."
	cd terraform && terraform init && terraform apply -auto-approve
	@echo "Infrastructure provisioned successfully!"

destroy-infra:
	@echo "Destroying infrastructure..."
	aws ecr delete-repository --repository-name lambda-container --force
	cd terraform && terraform destroy -auto-approve
	@echo "Infrastructure destroyed successfully!"