import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('fitness-user-assessments')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))
    
    # Handle CORS preflight
    if event.get('requestContext', {}).get('http', {}).get('method') == 'OPTIONS':
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET, OPTIONS"
            }
        }
    
    try:
        # Get user_id from query parameters
        user_id = event.get('queryStringParameters', {}).get('user_id') if event.get('queryStringParameters') else None
        
        if not user_id:
            return {
                "statusCode": 400,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type"
                },
                "body": json.dumps({"error": "Missing user_id parameter"})
            }
        
        # Query DynamoDB for user's assessment history
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False,  # Sort by timestamp descending (newest first)
            Limit=15  # Limit to last 15 assessments
        )
        
        assessments = []
        for item in response['Items']:
            assessments.append({
                'timestamp': item['timestamp'],
                'question': item['question'],
                'assessment_type': item['assessment_type'],
                'ai_response': item['ai_response'],
                'user_data': json.loads(item.get('user_data', '{}')) if item.get('user_data') else {}
            })
        
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET, OPTIONS"
            },
            "body": json.dumps({
                "user_id": user_id,
                "assessments": assessments,
                "count": len(assessments)
            })
        }
        
    except Exception as e:
        print("Error occurred:", str(e))
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"error": "Internal server error", "details": str(e)})
        }