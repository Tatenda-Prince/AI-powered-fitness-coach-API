@echo off
echo Uploading website to S3...

cd terraform

echo Getting S3 bucket name...
for /f "tokens=*" %%i in ('terraform output -raw s3_bucket_name') do set S3_BUCKET=%%i
for /f "tokens=*" %%i in ('terraform output -raw api_endpoint') do set API_ENDPOINT=%%i

echo Updating frontend config...
cd ../frontend
echo window.CONFIG = { > config.js
echo     API_URL: '%API_ENDPOINT%' >> config.js
echo }; >> config.js

echo Uploading files to S3 bucket: %S3_BUCKET%
aws s3 sync . s3://%S3_BUCKET%/ --delete

echo Upload complete!
for /f "tokens=*" %%i in ('cd ../terraform && terraform output -raw website_url') do set WEBSITE_URL=%%i
echo Website available at: %WEBSITE_URL%

pause