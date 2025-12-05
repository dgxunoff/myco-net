# 🚀 AWS Deployment Guide for MycoShield

## Quick Start - 3 Options

### ⚡ Option 1: EC2 (EASIEST - 10 minutes)

**Step 1: Launch EC2 Instance**
```bash
# Go to AWS Console > EC2 > Launch Instance
# Choose: Amazon Linux 2023
# Instance type: t3.medium (2 vCPU, 4GB RAM)
# Security Group: Allow ports 22 (SSH) and 80 (HTTP)
# Create and download key pair
```

**Step 2: Connect and Deploy**
```bash
# SSH into instance
ssh -i your-key.pem ec2-user@YOUR_EC2_IP

# Install Docker
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo usermod -a -G docker ec2-user
newgrp docker

# Clone and run
git clone https://github.com/YOUR_USERNAME/MycoNet.git
cd MycoNet

# Build Docker image
docker build -t mycoshield .

# Run container
docker run -d -p 80:8501 \
  -e APTOS_PRIVATE_KEY="ed25519-priv-0xd54d7b599c6b2b2f1d094e4073c1055440dad8ad5b622020ce2140e615891250" \
  --restart unless-stopped \
  mycoshield

# Check status
docker ps
```

**Access**: `http://YOUR_EC2_PUBLIC_IP`

**Cost**: ~$30/month (t3.medium)

---

### 🐳 Option 2: ECS Fargate (SERVERLESS - 20 minutes)

**Step 1: Install AWS CLI**
```bash
# Windows
msiexec.exe /i https://awscli.amazonaws.com/AWSCLIV2.msi

# Configure
aws configure
# Enter: Access Key, Secret Key, Region (us-east-1)
```

**Step 2: Push to ECR**
```bash
cd c:\Users\admin\Desktop\MycoNet

# Create ECR repository
aws ecr create-repository --repository-name mycoshield --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t mycoshield .
docker tag mycoshield:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/mycoshield:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/mycoshield:latest
```

**Step 3: Create ECS Service (AWS Console)**
1. Go to ECS > Create Cluster > Fargate
2. Create Task Definition using `aws-ecs-task-definition.json`
3. Create Service with Load Balancer
4. Access via Load Balancer DNS

**Cost**: ~$50/month (pay per use)

---

### 🌱 Option 3: Elastic Beanstalk (MANAGED - 15 minutes)

**Step 1: Install EB CLI**
```bash
pip install awsebcli
```

**Step 2: Deploy**
```bash
cd c:\Users\admin\Desktop\MycoNet

# Initialize
eb init -p docker mycoshield --region us-east-1

# Create environment
eb create mycoshield-env --instance-type t3.medium

# Deploy
eb deploy

# Open in browser
eb open
```

**Cost**: ~$35/month (includes load balancer)

---

## 💰 Cost Comparison

| Option | Monthly Cost | Setup Time | Auto-Scaling |
|--------|-------------|------------|--------------|
| EC2 | $30 | 10 min | No |
| ECS Fargate | $50 | 20 min | Yes |
| Elastic Beanstalk | $35 | 15 min | Yes |

---

## 🔥 Recommended: EC2 (Simplest)

**Full Commands:**
```bash
# 1. Launch EC2 t3.medium in AWS Console
# 2. SSH in:
ssh -i key.pem ec2-user@YOUR_IP

# 3. Run this:
sudo yum update -y && \
sudo yum install -y docker git && \
sudo service docker start && \
sudo usermod -a -G docker ec2-user && \
newgrp docker && \
git clone https://github.com/YOUR_REPO/MycoNet.git && \
cd MycoNet && \
docker build -t mycoshield . && \
docker run -d -p 80:8501 \
  -e APTOS_PRIVATE_KEY="YOUR_KEY" \
  --restart unless-stopped \
  mycoshield

# 4. Access: http://YOUR_EC2_IP
```

---

## 🛠️ Troubleshooting

**Port 8501 not accessible?**
- Check EC2 Security Group allows port 80 inbound

**Docker permission denied?**
```bash
sudo usermod -a -G docker ec2-user
newgrp docker
```

**Out of memory?**
- Use t3.medium or larger (4GB+ RAM)

**Blockchain features not working?**
- Normal - Aptos CLI not in container
- App will work but show cached blockchain values

---

## 📊 What Works on AWS

✅ AI threat detection  
✅ 3D visualization  
✅ Demo traffic generation  
✅ PCAP file upload  
⚠️ Blockchain (cached values only)  
⚠️ Firewall blocking (requires host access)

---

## 🎯 Next Steps

1. **Push to GitHub** (if not already)
2. **Choose deployment option** (EC2 recommended)
3. **Follow steps above**
4. **Share the public URL!**

**Need help?** Let me know which option you want to use!
