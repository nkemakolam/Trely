import os
import random
from flask import Flask, render_template
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

# Azure Storage connection settings
AZURE_CONNECTION_STRING = "Your_Azure_Storage_Connection_String"
CONTAINER_NAME = "your-container-name"

# Initialize BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)


def get_files_list():
    """Retrieve a list of images and videos from the Azure container."""
    blob_list = container_client.list_blobs()
    media_files = []

    # Filter only image and video files
    for blob in blob_list:
        if blob.name.endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov')):
            media_files.append(blob.name)

    return media_files


@app.route('/')
def index():
    files = get_files_list()
    if files:
        random_file = random.choice(files)  # Pick a random file
        file_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/{random_file}"
        return render_template('index.html', file_url=file_url)
    else:
        return "No media files found."


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
