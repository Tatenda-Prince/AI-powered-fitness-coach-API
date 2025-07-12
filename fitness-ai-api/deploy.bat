@echo off
echo ========================================
echo   AI Fitness Coach - Full Deployment
echo ========================================

echo Step 1: Creating Lambda deployment packages...
cd lambda_functions

echo Packaging fitness_coach.py with dependencies...
powershell -Command "Compress-Archive -Path fitness_coach.py,* -DestinationPath ../fitness_coach.zip -Force"

echo Packaging user_history.py...
powershell -Command "Compress-Archive -Path user_history.py -DestinationPath ../user_history.zip -Force"

cd ../terraform

echo Step 2: Deploying infrastructure with Terraform...
terraform init
terraform plan
terraform apply -auto-approve

echo Step 3: Getting deployment outputs...
for /f "tokens=*" %%i in ('terraform output -raw api_endpoint') do set API_ENDPOINT=%%i
for /f "tokens=*" %%i in ('terraform output -raw s3_bucket_name') do set S3_BUCKET=%%i
for /f "tokens=*" %%i in ('terraform output -raw website_url') do set WEBSITE_URL=%%i

echo Step 4: Updating frontend configuration...
cd ../frontend
echo window.CONFIG = { > config.js
echo     API_URL: '%API_ENDPOINT%' >> config.js
echo }; >> config.js

echo Step 5: Uploading website to S3...
aws s3 sync . s3://%S3_BUCKET%/ --delete

echo ========================================
echo   Deployment Complete!
echo ========================================
echo API Endpoint: %API_ENDPOINT%
echo Website URL:  %WEBSITE_URL%
echo S3 Bucket:    %S3_BUCKET%
echo ========================================
echo.
echo Your fitness coach is now live!
echo Open: %WEBSITE_URL%
echo.
pause