#!/bin/bash
# EC2 User Data Script - Auto-deploy MycoShield on launch

# Update system
yum update -y

# Install Docker
yum install -y docker git
service docker start
usermod -a -G docker ec2-user

# Clone repository (UPDATE THIS URL)
cd /home/ec2-user
git clone https://github.com/YOUR_USERNAME/MycoNet.git
cd MycoNet

# Build Docker image
docker build -t mycoshield .

# Run container
docker run -d -p 80:8501 \
  -e APTOS_PRIVATE_KEY="ed25519-priv-0xd54d7b599c6b2b2f1d094e4073c1055440dad8ad5b622020ce2140e615891250" \
  --restart unless-stopped \
  mycoshield

# Log completion
echo "MycoShield deployed successfully!" > /home/ec2-user/deployment.log
