#!/bin/bash

# MycoShield AWS Deployment Script
# Choose your deployment method below

echo "🍄 MycoShield AWS Deployment"
echo "=============================="

# Configuration
AWS_REGION="us-east-1"
ECR_REPO="mycoshield"
ECS_CLUSTER="mycoshield-cluster"
ECS_SERVICE="mycoshield-service"

# ============================================
# OPTION 1: Deploy to EC2 (Simplest)
# ============================================
deploy_ec2() {
    echo "📦 Deploying to EC2..."
    
    # 1. Launch EC2 instance (t3.medium recommended)
    # 2. SSH into instance
    # 3. Run these commands:
    
    cat << 'EOF'
# On EC2 instance:
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -a -G docker ec2-user

# Clone repo
git clone YOUR_GITHUB_REPO
cd MycoNet

# Build and run
sudo docker build -t mycoshield .
sudo docker run -d -p 80:8501 \
  -e APTOS_PRIVATE_KEY="YOUR_KEY" \
  --restart unless-stopped \
  mycoshield

# Access at: http://YOUR_EC2_PUBLIC_IP
EOF
}

# ============================================
# OPTION 2: Deploy to ECS Fargate (Serverless)
# ============================================
deploy_ecs() {
    echo "🚀 Deploying to ECS Fargate..."
    
    # 1. Create ECR repository
    aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION
    
    # 2. Get ECR login
    aws ecr get-login-password --region $AWS_REGION | \
        docker login --username AWS --password-stdin \
        $(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com
    
    # 3. Build and push image
    docker build -t $ECR_REPO .
    ECR_URI=$(aws sts get-caller-identity --query Account --output text).dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
    docker tag $ECR_REPO:latest $ECR_URI
    docker push $ECR_URI
    
    echo "✅ Image pushed to ECR: $ECR_URI"
    echo "📝 Update aws-ecs-task-definition.json with this URI"
    echo "🌐 Then create ECS service in AWS Console"
}

# ============================================
# OPTION 3: Deploy to Elastic Beanstalk
# ============================================
deploy_eb() {
    echo "🌱 Deploying to Elastic Beanstalk..."
    
    # Initialize EB
    eb init -p docker mycoshield --region $AWS_REGION
    
    # Create environment
    eb create mycoshield-env --instance-type t3.medium
    
    # Deploy
    eb deploy
    
    # Open in browser
    eb open
}

# ============================================
# Main Menu
# ============================================
echo ""
echo "Choose deployment option:"
echo "1) EC2 (Simplest - Manual setup)"
echo "2) ECS Fargate (Serverless - Auto-scaling)"
echo "3) Elastic Beanstalk (Managed - Easy)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1) deploy_ec2 ;;
    2) deploy_ecs ;;
    3) deploy_eb ;;
    *) echo "Invalid choice" ;;
esac
