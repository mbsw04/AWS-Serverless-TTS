import json
import boto3
from botocore.exceptions import ClientError
import os

# Initialize S3 client
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract S3 object key from event
        s3_key = event['s3Key']
        if not s3_key:
            raise ValueError("Missing required parameter: s3Key")

        print(f"Attempting to delete file from S3: Bucket={os.environ['buc_name']}, Key={s3_key}")

        # Delete the file from S3
        s3_bucket_name = os.environ['buc_name']
        s3_client.delete_object(Bucket=s3_bucket_name, Key=s3_key)
        print(f"File deleted successfully from S3: Bucket={s3_bucket_name}, Key={s3_key}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'File deleted successfully'
            })
        }

    except Exception as e:
        print(f"Exception: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f"An unexpected error occurred: {str(e)}"
            })
        }
