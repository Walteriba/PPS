import cloudinary
import cloudinary.uploader
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def subir_y_obtener_url(archivo_o_ruta, nombre_identificador):
    try:
        resultado = cloudinary.uploader.upload(archivo_o_ruta, public_id=nombre_identificador)
        return resultado.get("secure_url")
    except Exception as e:
        raise RuntimeError(f"Falló la subida a Cloudinary: {e}") from e