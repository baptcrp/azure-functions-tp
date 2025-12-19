import azure.functions as func
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
import json, os

def main(req: func.HttpRequest) -> func.HttpResponse:
    conn_str = os.environ["AzureWebJobsStorage"]
    blob_service_client = BlobServiceClient.from_connection_string(conn_str)
    container_client = blob_service_client.get_container_client("thumbnails")
    
    # Extraction des clés pour le jeton SAS
    account_name = blob_service_client.account_name
    account_key = conn_str.split("AccountKey=")[1].split(";")[0]

    urls = []
    for blob in container_client.list_blobs():
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name="thumbnails",
            blob_name=blob.name,
            account_key=account_key,
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=2)
        )
        urls.append(f"https://{account_name}.blob.core.windows.net/thumbnails/{blob.name}?{sas_token}")
    
    return func.HttpResponse(json.dumps(urls), mimetype="application/json")