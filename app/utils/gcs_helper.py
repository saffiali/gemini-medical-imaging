import os
from google.cloud import storage

def get_storage_client():
    """Returns a Google Cloud Storage client."""
    # Assumes environment is authenticated (e.g. running on Cloud Run or local ADC)
    return storage.Client()

def list_blobs(bucket_name, prefix=None):
    """Lists blobs in a bucket, optionally filtering by prefix."""
    client = get_storage_client()
    try:
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)
        return [blob.name for blob in blobs]
    except Exception as e:
        print(f"Error listing blobs from bucket {bucket_name}: {e}")
        return []

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    client = get_storage_client()
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
        return True
    except Exception as e:
        print(f"Error downloading blob {source_blob_name}: {e}")
        return False

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    client = get_storage_client()
    try:
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name)
        return True
    except Exception as e:
        print(f"Error uploading blob {destination_blob_name}: {e}")
        return False
