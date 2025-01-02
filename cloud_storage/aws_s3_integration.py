import boto3
import json

def upload_to_s3():
    """Function to upload a file to AWS S3."""
    s3 = boto3.client('s3')
    bucket_name = "example-bucket"
    object_name = "example_object.json"

    # Data to upload
    data = [{'id': i, 'value': f'message {i}'} for i in range(10)]

    try:
        s3.create_bucket(Bucket=bucket_name)
    except Exception as e:
        print(f"Bucket might already exist: {e}")

    s3.put_object(Bucket=bucket_name, Key=object_name, Body=json.dumps(data))
    print(f"Uploaded data to S3 object: {object_name}")

def download_from_s3():
    """Function to download a file from AWS S3."""
    s3 = boto3.client('s3')
    bucket_name = "example-bucket"
    object_name = "example_object.json"

    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_name)
        data = json.loads(response['Body'].read().decode('utf-8'))
        print(f"Downloaded data: {data}")
    except Exception as e:
        print(f"Error downloading object: {e}")

def main():
    choice = input("Enter 'u' to upload to S3 or 'd' to download from S3: ").strip().lower()

    if choice == 'u':
        upload_to_s3()
    elif choice == 'd':
        download_from_s3()
    else:
        print("Invalid choice. Please enter 'u' or 'd'.")

if __name__ == "__main__":
    main()
