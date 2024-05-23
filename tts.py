import boto3
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

def text_to_speech(text, output_file):
    # Initialize the Polly client
    region_name = os.getenv('AWS_REGION')
    polly = boto3.client('polly', region_name=region_name)
    
    # Call Polly's synthesize_speech API
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Joanna'  # Change the voice ID as per your preference
    )
    
    # Save audio to local file
    with open(output_file, 'wb') as file:
        file.write(response['AudioStream'].read())
    
    return response

def upload_to_s3(file_path, bucket_name, object_name):
    # Initialize the S3 client with loaded credentials
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    region_name = os.getenv('AWS_REGION')
    s3 = boto3.client('s3', 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key,
                      region_name=region_name)
    
    # Upload the file to S3 with timestamp in object name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    object_name_with_timestamp = f"{timestamp}_{object_name}"
    s3.upload_file(file_path, bucket_name, object_name_with_timestamp)

if __name__ == "__main__":
    text = "Hello, this is a sample text. This text will be converted to speech using AWS Polly."
    output_file = "output.mp3"
    bucket_name = "your-s3-bucket"
    object_name = "output.mp3"
    
    # Convert text to speech and save locally
    response = text_to_speech(text, output_file)
    print("Audio saved locally:", output_file)
    
    # Upload audio to S3
    upload_to_s3(output_file, bucket_name, object_name)
    print("Audio uploaded to S3")
