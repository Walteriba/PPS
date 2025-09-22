
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

def subir_y_obtener_url(ruta_archivo_local, nombre_identificador):
    """
    Sube un archivo (imagen, video, etc.) a Cloudinary y devuelve su URL pública.

    Args:
        ruta_archivo_local (str): La ruta completa al archivo en tu sistema local.
        nombre_identificador (str): Un nombre único para el archivo en Cloudinary.

    Returns:
        str: La URL segura de la imagen subida, o None si ocurre un error.
    """
    try:
        resultado = cloudinary.uploader.upload(ruta_archivo_local, public_id=nombre_identificador)
        return resultado["secure_url"]
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo_local}' no se encontró.")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al subir el archivo: {e}")
        return None
