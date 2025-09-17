#!/bin/bash

# Manual deployment script
# Use this when you want to deploy without GitHub Actions

set -e

echo "🚀 Manually deploying Flask app to AWS Lambda..."

# Configuration
AWS_REGION="us-east-1"
ECR_REPO_NAME="simple-flask-app"
LAMBDA_FUNCTION_NAME="simple-flask-app"

# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

echo "📦 Building Docker image..."
docker build -t $ECR_REPO_NAME .

echo "🔐 Logging in to ECR..."
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

echo "📤 Pushing to ECR..."
IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest"
docker tag $ECR_REPO_NAME:latest $IMAGE_URI
docker push $IMAGE_URI

echo "⚡ Updating Lambda function..."
aws lambda update-function-code \
    --function-name $LAMBDA_FUNCTION_NAME \
    --image-uri $IMAGE_URI

echo "⏳ Waiting for update to complete..."
aws lambda wait function-updated --function-name $LAMBDA_FUNCTION_NAME

echo "✅ Deployment completed successfully!"
echo "🌐 Your API is now updated with the latest code."