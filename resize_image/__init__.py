import azure.functions as func
from PIL import Image
import io

def main(myblob: func.InputStream, outputblob: func.Out[bytes]):
    img = Image.open(myblob)
    img.thumbnail((256, 256)) # Redimensionnement
    
    img_byte_arr = io.BytesIO()
    # On garde le format d'origine (PNG/JPEG)
    img.save(img_byte_arr, format=img.format if img.format else 'JPEG')
    outputblob.set(img_byte_arr.getvalue())