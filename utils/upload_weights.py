# pip install azure-storage-blob azure-identity (not installed in the container)
# curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash (for login and authetization)

import os, uuid
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def upload_weights(blob_path, local_path, local_fname, blob_fname=None, container_name="data", project_name="vibratorvials"):
    """
    Uploads the weights to Azure Storage Explorer.
    """
    account_url = f"https://{project_name}.blob.core.windows.net"
    default_credential = DefaultAzureCredential()

    # on the blob
    if blob_fname is None:
        blob_fname = local_fname
    path2blob = os.path.join(blob_path, blob_fname)
    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=path2blob)

    # local
    print(f"Uploading to Azure Storage as blob:\n\t{local_fname}")
    path2file = os.path.join(local_path, local_fname)
    with open(file=path2file, mode="rb") as data:
        blob_client.upload_blob(data)


def download_weights(blob_path, local_path, blob_fname, local_fname=None, container_name="data", project_name="vibratorvials"):
    """
    Download the weights from Azure Storage Explorer
    """
    if local_fname is None:
        local_fname = blob_fname
    path2blob = os.path.join(blob_path, blob_fname)
    path2local = os.path.joim(local_path, local_fname)

    blob_service_client = BlobServiceClient(account_url, credential=default_credential)
    container_client = blob_service_client.get_container_client(container=container_name)

    print("\nDownloading blob to \n\t" + local_fname)
    with open(file=download_file_path, mode="wb") as download_file:
        download_file.write(container_client.download_blob(blob.name).readall())