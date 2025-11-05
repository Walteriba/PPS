import os
from datetime import datetime

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

load_dotenv()

# Configuración de Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True,
)

# Función para subir archivo a Cloudinary y obtener la URL
def subir_y_obtener_url(archivo_o_ruta):
    try:
        resultado = cloudinary.uploader.upload(
            archivo_o_ruta, public_id=f"{datetime.now().timestamp()}"
        )
        return resultado.get("secure_url")
    except Exception as e:
        raise RuntimeError(f"Falló la subida a Cloudinary: {e}") from e
