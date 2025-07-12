# 🏋️ AI-Powered Fitness Assessment Platform

[![AWS](https://img.shields.io/badge/AWS-Cloud-orange)](https://aws.amazon.com/)
[![Terraform](https://img.shields.io/badge/Terraform-IaC-purple)](https://terraform.io/)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org/)
[![Serverless](https://img.shields.io/badge/Architecture-Serverless-green)](https://aws.amazon.com/serverless/)

A production-ready, serverless fitness assessment platform that provides personalized health and fitness calculations using scientific formulas. Built with modern DevOps practices and deployed on AWS cloud infrastructure.

## 🎯 Background

The fitness industry often requires expensive equipment or personal trainer consultations to get accurate fitness assessments. This project democratizes access to professional-grade fitness calculations by providing:

- **VO2 Max estimation** using age-based formulas
- **BMR and calorie calculations** using Mifflin-St Jeor equation
- **Heart rate zone calculations** for optimal training
- **BMI assessments** with health recommendations
- **User tracking and history** for progress monitoring

## 📋 Project Overview

This is a full-stack serverless application that demonstrates modern cloud architecture and DevOps practices. The system processes natural language fitness questions and returns scientifically accurate assessments with personalized recommendations.

**Live Demo**: [https://d138ljgsl2hkcc.cloudfront.net](https://d138ljgsl2hkcc.cloudfront.net)

### Architecture Diagram
```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│   CloudFront│────│  S3 Website  │    │ API Gateway │────│   Lambda    │
│     CDN     │    │   Frontend   │    │   Routes    │    │ Functions   │
└─────────────┘    └──────────────┘    └─────────────┘    └─────────────┘
                                              │                    │
                                              │                    │
                                       ┌─────────────┐    ┌─────────────┐
                                       │  DynamoDB   │    │ CloudWatch  │
                                       │  Database   │    │   Logging   │
                                       └─────────────┘    └─────────────┘
```

## 🎯 Project Objectives

- **Demonstrate serverless architecture** using AWS Lambda and API Gateway
- **Implement Infrastructure as Code** using Terraform
- **Create production-ready application** with proper error handling and logging
- **Showcase DevOps best practices** with automated deployment
- **Provide real business value** through accurate fitness assessments
- **Optimize for cost** using pay-per-use serverless model

## ✨ Features

### 🧮 Fitness Calculations
- **VO2 Max Estimation**: Cardiovascular fitness assessment
- **BMR & TDEE**: Metabolic rate and daily calorie needs
- **BMI Calculator**: Body mass index with health categories
- **Heart Rate Zones**: Training zones for optimal workouts
- **Personalized Recommendations**: Based on user profile

### 🔧 Technical Features
- **Serverless Architecture**: Auto-scaling, pay-per-use
- **Global CDN**: Fast content delivery worldwide
- **User Tracking**: Assessment history and progress monitoring
- **RESTful API**: Clean, documented endpoints
- **CORS Enabled**: Cross-origin resource sharing
- **Error Handling**: Comprehensive error management
- **Logging**: CloudWatch integration for monitoring

### 🌐 User Experience
- **Responsive Design**: Works on all devices
- **Natural Language**: Ask questions in plain English
- **Quick Actions**: Pre-defined question buttons
- **History Viewer**: Track assessment progress
- **Real-time Results**: Instant calculations

## 🛠️ Technologies Used

### **Cloud Infrastructure**
- **AWS Lambda**: Serverless compute functions
- **API Gateway**: RESTful API management
- **DynamoDB**: NoSQL database for user data
- **S3**: Static website hosting
- **CloudFront**: Global content delivery network
- **CloudWatch**: Logging and monitoring
- **IAM**: Identity and access management

### **Infrastructure as Code**
- **Terraform**: Infrastructure provisioning and management
- **AWS Provider**: Terraform AWS integration

### **Development**
- **Python 3.11**: Backend logic and calculations
- **JavaScript**: Frontend interactivity
- **HTML/CSS**: User interface design
- **JSON**: Data exchange format

### **DevOps Tools**
- **AWS CLI**: Command-line interface
- **Git**: Version control (ready)
- **PowerShell**: Deployment automation

## 💼 Use Cases

### **Personal Fitness**
- Individual fitness tracking and goal setting
- Home workout planning and optimization
- Health metric monitoring and progress tracking

### **Professional Applications**
- Gym and fitness center client assessments
- Personal trainer consultation tools
- Corporate wellness program platforms
- Healthcare provider fitness screening

### **Business Integration**
- Fitness app backend API
- Wearable device data processing
- Health insurance risk assessment
- Telemedicine platform integration

## 📋 Prerequisites

### **Required Software**
- [AWS CLI](https://aws.amazon.com/cli/) configured with credentials
- [Terraform](https://terraform.io/downloads.html) v1.0+
- [PowerShell](https://docs.microsoft.com/en-us/powershell/) (Windows)
- [Git](https://git-scm.com/) for version control

### **AWS Account Setup**
- AWS account with appropriate permissions
- IAM user with programmatic access
- AWS CLI configured with credentials

### **Required AWS Permissions**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:*",
        "apigateway:*",
        "dynamodb:*",
        "s3:*",
        "cloudfront:*",
        "iam:*",
        "logs:*"
      ],
      "Resource": "*"
    }
  ]
}
```

## 🚀 Terraform Workflow

### **1. Initialize Terraform**
```bash
cd terraform
terraform init
```
This downloads required providers and initializes the backend.

### **2. Validate Configuration**
```bash
terraform validate
```
Checks syntax and validates configuration files.

### **3. Plan Infrastructure**
```bash
terraform plan
```
Shows what resources will be created, modified, or destroyed.

### **4. Apply Infrastructure**
```bash
terraform apply
```
Creates the infrastructure. Type `yes` when prompted.

### **5. Get Outputs**
```bash
terraform output
```
Displays important URLs and resource names:
- `api_endpoint`: API Gateway URL
- `website_url`: CloudFront distribution URL
- `s3_bucket_name`: S3 bucket for frontend files

## 🧪 Testing the System

### **1. Automated Deployment**
```bash
# Run the complete deployment script
./deploy.bat
```

### **2. Manual Testing Steps**

#### **Frontend Testing**
1. Open the CloudFront URL from terraform output
2. Fill in user profile (age, weight, height, gender, activity level)
3. Test sample questions:
   - "What is my VO2 max?"
   - "How many calories should I eat per day?"
   - "What's my BMI?"
   - "What are my heart rate zones?"

#### **API Testing**
```bash
# Test API directly
curl -X POST [API_ENDPOINT]/coach \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is my VO2 max?",
    "user_data": {
      "age": 25,
      "weight": 75,
      "height": 180,
      "gender": "male",
      "activity_level": "very"
    }
  }'
```

#### **History Testing**
```bash
# Test user history endpoint
curl -X GET "[API_ENDPOINT]/history?user_id=[USER_ID]"
```

### **3. Monitoring and Logs**
```bash
# View Lambda logs
aws logs describe-log-groups --log-group-name-prefix "/aws/lambda/fitness"

# Get recent log events
aws logs get-log-events --log-group-name "/aws/lambda/fitness-coach-api" --log-stream-name [STREAM_NAME]
```

## 📊 CI/CD System Applications

### **Current Implementation**
- **Infrastructure as Code**: Terraform manages all resources
- **Automated Deployment**: PowerShell scripts for complete deployment
- **Version Control Ready**: Git-friendly project structure
- **Environment Separation**: Configurable for dev/staging/prod

### **CI/CD Enhancement Opportunities**
```yaml
# Example GitHub Actions workflow
name: Deploy Fitness Platform
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v1
      - name: Terraform Apply
        run: |
          cd terraform
          terraform init
          terraform apply -auto-approve
      - name: Deploy Frontend
        run: |
          aws s3 sync frontend/ s3://${{ env.S3_BUCKET }}/
```

### **Monitoring Integration**
- **CloudWatch Dashboards**: Custom metrics and alarms
- **Error Tracking**: Automated error notifications
- **Performance Monitoring**: Response time and usage analytics
- **Cost Monitoring**: AWS billing alerts and optimization

## 📈 Performance Metrics

- **Response Time**: < 200ms average
- **Availability**: 99.9% uptime (AWS SLA)
- **Scalability**: Auto-scales to handle traffic spikes
- **Cost**: Pay-per-request, typically < $1/month for personal use

## 🔒 Security Features

- **IAM Roles**: Least privilege access
- **HTTPS Only**: SSL/TLS encryption
- **CORS Configuration**: Controlled cross-origin access
- **Input Validation**: Sanitized user inputs
- **No Sensitive Data**: No PII stored unnecessarily

## 📝 Project Structure

```
fitness-ai-api/
├── terraform/                 # Infrastructure as Code
│   ├── main.tf               # Main Terraform configuration
│   ├── variables.tf          # Input variables
│   └── outputs.tf            # Output values
├── lambda_functions/          # Serverless functions
│   ├── fitness_coach.py      # Main assessment logic
│   └── user_history.py       # History retrieval
├── frontend/                  # Web application
│   ├── index.html            # Main webpage
│   └── config.js             # API configuration
├── deploy.bat                 # Deployment automation
└── README.md                 # Project documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

For questions or support:
- Create an issue in the repository
- Check CloudWatch logs for debugging
- Review Terraform documentation for infrastructure questions

---

**Built with ❤️ using AWS Serverless Architecture and Modern DevOps Practices**