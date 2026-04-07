import json
import boto3


rekognition = boto3.client('rekognition')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
    except json.JSONDecodeError:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid JSON in request body'})
        }
    
    bucket_name = body.get("bucket_name")
    key = body.get("key")
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': key
            }
        },
        MaxLabels=10,
        MinConfidence=75
    )
    labels = response.get('Labels', [])
    formatted_labels = [{'Name': label['Name'], 'Confidence': label['Confidence']} for label in labels] 
    return {
        'statusCode': 200,
        'body': json.dumps({'labels': formatted_labels})
    }