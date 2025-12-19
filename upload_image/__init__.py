import azure.functions as func
from azure.storage.blob import BlobServiceClient
import os

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file = req.files.get('file')
        if not file:
            return func.HttpResponse("Aucun fichier trouvé", status_code=400)

        conn_str = os.environ["AzureWebJobsStorage"]
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        blob_client = blob_service_client.get_blob_client(container="images", blob=file.filename)
        
        blob_client.upload_blob(file.read(), overwrite=True)
        return func.HttpResponse("Succès", status_code=200)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=500)