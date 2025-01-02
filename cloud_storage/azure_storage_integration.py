from azure.storage.blob import BlobServiceClient
import json

def upload_to_azure():
    """Function to upload a file to Azure Blob Storage."""
    connection_string = "<your_connection_string>"
    container_name = "example-container"
    blob_name = "example_blob.json"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Create container if it does not exist
    try:
        container_client.create_container()
    except Exception as e:
        print(f"Container might already exist: {e}")

    # Data to upload
    data = [{'id': i, 'value': f'message {i}'} for i in range(10)]
    blob_client = container_client.get_blob_client(blob_name)

    blob_client.upload_blob(json.dumps(data), overwrite=True)
    print(f"Uploaded data to blob: {blob_name}")

def download_from_azure():
    """Function to download a file from Azure Blob Storage."""
    connection_string = "<your_connection_string>"
    container_name = "example-container"
    blob_name = "example_blob.json"

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)

    downloaded_blob = blob_client.download_blob().readall()
    data = json.loads(downloaded_blob)
    print(f"Downloaded data: {data}")

def main():
    choice = input("Enter 'u' to upload to Azure or 'd' to download from Azure: ").strip().lower()

    if choice == 'u':
        upload_to_azure()
    elif choice == 'd':
        download_from_azure()
    else:
        print("Invalid choice. Please enter 'u' or 'd'.")

if __name__ == "__main__":
    main()
