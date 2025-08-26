# 🏋️ AI-Powered Fitness Assessment Platform
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


### Architecture Diagram

<<<<<<< HEAD
![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/0aab79f913327e758671d991ef5ca73e1555cd74/fitness-ai-api/img/Screenshot%202025-07-12%20202007.png)
=======
>>>>>>> 095b3eb (modified readme file)

## 🎯 Project Objectives

- **Demonstrate serverless architecture** using AWS Lambda and API Gateway
- **Implement Infrastructure as Code** using Terraform
- **Create production-ready application** with proper error handling and logging
- **Showcase DevOps best practices** with automated deployment
- **Provide real business value** through accurate fitness assessments
- **Optimize for cost** using pay-per-use serverless model

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



## 📋 Prerequisites

### **Required Software**
- [AWS CLI](https://aws.amazon.com/cli/) configured with credentials
- [Terraform](https://terraform.io/downloads.html) v1.0+
- [Linux] (Windows WSL)
- [Git](https://git-scm.com/) for version control

```bash
git clone https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API.git
```
### **AWS Account Setup**
- AWS account with appropriate permissions
- IAM user with programmatic access
- AWS CLI configured with credentials



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

  ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/9dec632b7554fb1ac252421724af05e535f78d28/fitness-ai-api/img/Screenshot%202025-07-12%20231958.png)


## Testing the System


### **1. Manual Testing Steps**

#### **Frontend Testing**
1. Open the CloudFront URL from terraform output
2. Fill in user profile (age, weight, height, gender, activity level)
3. Test sample questions:

   - **"What is my VO2 max?"**

   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/3e1c0cf2296807e8e77636420622bbe68ff1258a/fitness-ai-api/img/Screenshot%202025-07-12%20230434.png)


   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/73c11e7271dfd4cb2f6cf840aa2c989f9862b9fb/fitness-ai-api/img/Screenshot%202025-07-12%20230938.png)


   - **"How many calories should I eat per day?"**

   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/b1fad2fccc18e7e6178d2b658a49de44fa1be7bb/fitness-ai-api/img/Screenshot%202025-07-12%20231010.png)


   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/7d763775b9b168509eba824a95b6d577f4a8fb59/fitness-ai-api/img/Screenshot%202025-07-12%20231033.png)


   - **"What's my BMI?"**

   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/4f9a35deee2d35c5b932466d73a270d7f91b7b75/fitness-ai-api/img/Screenshot%202025-07-12%20231112.png)



   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/9c52f60424f4e92ff14e6c360add7b9f49ff1f5c/fitness-ai-api/img/Screenshot%202025-07-12%20231124.png)


   - **"What are my heart rate zones?"**

   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/aa495a0ea0c6b8f9d0d515507199bf316f53cb73/fitness-ai-api/img/Screenshot%202025-07-12%20231213.png)



   ![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/34968282d9086f7a12f15eac3a5382f80bdd25c6/fitness-ai-api/img/Screenshot%202025-07-12%20231226.png)



### **Monitoring Integration**
- **CloudWatch Dashboards**: Custom metrics and alarms

![image_alt](https://github.com/Tatenda-Prince/AI-powered-fitness-coach-API/blob/a39b9f7a07668f77e56fdb9ac4598783a64e653f/fitness-ai-api/img/Screenshot%202025-07-12%20231914.png)

- **Error Tracking**: Automated error notifications

- **Performance Monitoring**: Response time and usage analytics

- **Cost Monitoring**: AWS billing alerts and optimization

## 📈 Performance Metrics

- **Response Time**: < 200ms average

- **Availability**: 99.9% uptime 

- **Scalability**: Auto-scales to handle traffic spikes

- **Cost**: Pay-per-request, typically < $1/month for personal use

## 🔒 Security Features

- **IAM Roles**: Least privilege access


