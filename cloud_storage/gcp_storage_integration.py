from google.cloud import storage
import json

def upload_to_gcs():
    """Function to upload a file to Google Cloud Storage."""
    client = storage.Client()
    bucket_name = "example-bucket"
    blob_name = "example_blob.json"

    bucket = client.bucket(bucket_name)

    # Create bucket if it does not exist
    try:
        bucket = client.create_bucket(bucket_name)
        print(f"Bucket {bucket_name} created.")
    except Exception as e:
        print(f"Bucket might already exist: {e}")

    # Data to upload
    data = [{'id': i, 'value': f'message {i}'} for i in range(10)]
    blob = bucket.blob(blob_name)
    blob.upload_from_string(json.dumps(data))
    print(f"Uploaded data to GCS blob: {blob_name}")

def download_from_gcs():
    """Function to download a file from Google Cloud Storage."""
    client = storage.Client()
    bucket_name = "example-bucket"
    blob_name = "example_blob.json"

    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    try:
        data = json.loads(blob.download_as_text())
        print(f"Downloaded data: {data}")
    except Exception as e:
        print(f"Error downloading blob: {e}")

def main():
    choice = input("Enter 'u' to upload to GCS or 'd' to download from GCS: ").strip().lower()

    if choice == 'u':
        upload_to_gcs()
    elif choice == 'd':
        download_from_gcs()
    else:
        print("Invalid choice. Please enter 'u' or 'd'.")

if __name__ == "__main__":
    main()
