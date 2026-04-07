import boto3
import requests
import os

from dotenv import load_dotenv
load_dotenv()

bucket_name = os.getenv('BUCKET_NAME')
api_url = os.getenv('API_URL')
file_path = os.getenv('FILE_PATH')
key = f"images/{os.path.basename(file_path)}"


s3 = boto3.client('s3')
# upload
s3.upload_file(file_path, bucket_name, key)

# call api
response = requests.post(api_url, json={
    'bucket_name': bucket_name,
    'key': key
})
data = response.json()

#Parse the response data
for label in data['labels']:
    print(f"Label: {label['Name']}, Confidence: {label['Confidence']:.2f}%")