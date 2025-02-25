import json
import boto3
import os
import tempfile
from botocore.exceptions import BotoCoreError, ClientError

# Initialize Polly and S3 clients
polly_client = boto3.client('polly')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    try:
        # Extract parameters from the event
        text = event.get('text')
        language = event.get('language')
        voice = event.get('voice')

        # Check if required parameters are provided
        if not text or not language or not voice:
            return {
                'statusCode': 400,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({'error': 'Missing required parameters'})
            }

        # Synthesize speech using Polly
        try:
            response = polly_client.synthesize_speech(
                Text=text, OutputFormat='mp3', VoiceId=voice, LanguageCode=language
            )
        except (BotoCoreError, ClientError) as e:
            return {
                'statusCode': 500,
                'headers': { "Access-Control-Allow-Origin": "*" },
                'body': json.dumps({'error': f"Polly API error: {str(e)}"})
            }

        # Save the speech audio to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as audio_file:
            audio_file.write(response['AudioStream'].read())
            audio_file_path = audio_file.name

        # Get the bucket name from the environment variable
        bucket_name = os.environ.get('buc_name')
        key = f"text-to-speech/{os.path.basename(audio_file_path)}"
        
        # Upload the file
        s3_client.upload_file(audio_file_path, bucket_name, key)
        
        # Cleanup temp file after uploading
        os.remove(audio_file_path)

        # Generate the S3 URL for the audio file
        audio_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"

        # Return the audio URL and S3 key
        return {
            'statusCode': 200,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({'audio_url': audio_url, 's3Key': key})
        }

    except Exception as e:
        # Catch any unexpected errors
        return {
            'statusCode': 500,
            'headers': { "Access-Control-Allow-Origin": "*" },
            'body': json.dumps({'error': str(e)})
        }
