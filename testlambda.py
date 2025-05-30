'''
testing the labda funtion tat counts the files in the bucket after fetching. 
finally deletes the files from the bucket
bucket name: testpracticumbucket
added the function to extract text from pdfs individually
'''


import json
import boto3
import pdfplumber
import io
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError

s3 = boto3.client('s3')
bucket_name = 'testpracticiumbucket'
folder_prefix = 'PilotPDFs/'

def list_files_in_bucket(bucket_name, prefix):
    paginator = s3.get_paginator('list_objects_v2')
    operation_parameters = {
        'Bucket': bucket_name,
        'Prefix': prefix
    }
    file_keys = []

    for page in paginator.paginate(**operation_parameters):
        if 'Contents' in page:
            for obj in page['Contents']:
                file_keys.append(obj['Key'])

    return file_keys

def delete_files_in_bucket(bucket_name, file_keys):
    for file_key in file_keys:
        try:
            s3.delete_object(Bucket=bucket_name, Key=file_key)
            print(f"Deleted file: {file_key}")
        except Exception as e:
            print(f"Error deleting file {file_key}: {e}")

def extract_text_from_pdf(pdf_bytes):
    text = ''
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text

def lambda_handler(event, context):
    try:
        print(f"Received event: {json.dumps(event)}")
        # List all files in the specified folder in the bucket
        file_keys = list_files_in_bucket(bucket_name, folder_prefix)
        total_files = len(file_keys)
        print(f"Total number of files in the bucket under {folder_prefix}: {total_files}")

        for file_key in file_keys:
            try:
                # Fetch the file from S3
                response = s3.get_object(Bucket=bucket_name, Key=file_key)
                pdf_bytes = response['Body'].read()

                # Extract text from the PDF
                text = extract_text_from_pdf(pdf_bytes)
                print(f"Extracted text from {file_key}: {text[:50]}")  # Print the first 100 characters of extracted text

                # Here you can handle the extracted text as needed, for example, store it in another S3 bucket

                # Delete the file after processing
                s3.delete_object(Bucket=bucket_name, Key=file_key)
                print(f"Deleted file: {file_key}")

            except Exception as e:
                print(f"Error processing file {file_key}: {e}")

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': f'All files in {folder_prefix} processed and deleted successfully',
                'total_files': total_files
            })
        }
    except NoCredentialsError as e:
        print("No credentials available: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps('No credentials error')
        }
    except PartialCredentialsError as e:
        print("Incomplete credentials: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Partial credentials error')
        }
    except ClientError as e:
        print("Client error: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps(f'Client error: {str(e)}')
        }
    except Exception as e:
        print("General error: ", e)
        return {
            'statusCode': 500,
            'body': json.dumps('Error processing files')
        }
