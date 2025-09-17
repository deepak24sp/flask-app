#!/bin/bash

# Simple Flask App AWS Setup Script
# Run this once to set up your AWS infrastructure

set -e  # Exit on any error

echo "🚀 Setting up AWS infrastructure for Simple Flask App..."

# Configuration
AWS_REGION="us-east-1"
ECR_REPO_NAME="simple-flask-app"
LAMBDA_FUNCTION_NAME="simple-flask-app"
LAMBDA_ROLE_NAME="simple-flask-app-role"

# Get AWS Account ID
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "📍 AWS Account ID: $AWS_ACCOUNT_ID"
echo "📍 Region: $AWS_REGION"

# Step 1: Create ECR Repository
echo "📦 Creating ECR repository..."
aws ecr create-repository \
    --repository-name $ECR_REPO_NAME \
    --region $AWS_REGION \
    --image-scanning-configuration scanOnPush=true \
    || echo "ECR repository might already exist"

# Step 2: Create IAM Role for Lambda
echo "🔐 Creating IAM role for Lambda..."
cat > trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

aws iam create-role \
    --role-name $LAMBDA_ROLE_NAME \
    --assume-role-policy-document file://trust-policy.json \
    || echo "Role might already exist"

# Attach basic Lambda execution policy
aws iam attach-role-policy \
    --role-name $LAMBDA_ROLE_NAME \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Step 3: Build and push initial Docker image
echo "🐳 Building and pushing initial Docker image..."
docker build -t $ECR_REPO_NAME .

# Login to ECR
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Tag and push image
IMAGE_URI="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO_NAME:latest"
docker tag $ECR_REPO_NAME:latest $IMAGE_URI
docker push $IMAGE_URI

# Step 4: Create Lambda function
echo "⚡ Creating Lambda function..."
aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --role arn:aws:iam::$AWS_ACCOUNT_ID:role/$LAMBDA_ROLE_NAME \
    --code ImageUri=$IMAGE_URI \
    --package-type Image \
    --timeout 30 \
    --memory-size 512 \
    --region $AWS_REGION \
    || echo "Lambda function might already exist"

# Step 5: Create API Gateway
echo "🌐 Creating API Gateway..."
API_ID=$(aws apigatewayv2 create-api \
    --name $LAMBDA_FUNCTION_NAME-api \
    --protocol-type HTTP \
    --target arn:aws:lambda:$AWS_REGION:$AWS_ACCOUNT_ID:function:$LAMBDA_FUNCTION_NAME \
    --query 'ApiId' \
    --output text)

echo "📡 API Gateway created with ID: $API_ID"

# Add permission for API Gateway to invoke Lambda
aws lambda add-permission \
    --function-name $LAMBDA_FUNCTION_NAME \
    --statement-id apigateway-invoke \
    --action lambda:InvokeFunction \
    --principal apigateway.amazonaws.com \
    --source-arn "arn:aws:execute-api:$AWS_REGION:$AWS_ACCOUNT_ID:$API_ID/*" \
    || echo "Permission might already exist"

# Step 6: Get API endpoint URL
API_ENDPOINT=$(aws apigatewayv2 get-api --api-id $API_ID --query 'ApiEndpoint' --output text)

# Cleanup temporary files
rm -f trust-policy.json

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📋 Summary:"
echo "   ECR Repository: $ECR_REPO_NAME"
echo "   Lambda Function: $LAMBDA_FUNCTION_NAME"
echo "   API Gateway ID: $API_ID"
echo "   API Endpoint: $API_ENDPOINT"
echo ""
echo "🧪 Test your API:"
echo "   curl $API_ENDPOINT/"
echo "   curl $API_ENDPOINT/todos"
echo ""
echo "🔧 Next steps:"
echo "   1. Set up GitHub secrets (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)"
echo "   2. Push your code to main branch"
echo "   3. Watch the GitHub Actions deploy your app!"