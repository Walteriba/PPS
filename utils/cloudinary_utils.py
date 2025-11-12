import os
import re
import time

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


def subir_y_obtener_url(archivo_storage):
    """
    Sube un archivo a Cloudinary:
    - Usa resource_type='raw' para PDFs, DOCX, ZIP, etc.
    - Genera un nombre limpio y único, conservando la extensión.
    - Devuelve la URL segura del archivo subido.
    """
    nombre_original = archivo_storage.filename
    nombre_lower = nombre_original.lower()
    base, extension = os.path.splitext(nombre_original)
    base_limpio = re.sub(r"[^a-zA-Z0-9_-]", "_", base)
    timestamp = int(time.time())

    extensiones_raw = (".pdf", ".doc", ".docx", ".zip", ".txt", ".xls", ".xlsx")
    tipo_recurso = "raw" if nombre_lower.endswith(extensiones_raw) else "image"

    if tipo_recurso == "image":
        public_id = f"{base_limpio}_{timestamp}"
    else:
        public_id = f"{base_limpio}_{timestamp}{extension}"

    try:
        resultado = cloudinary.uploader.upload(
            archivo_storage,
            resource_type=tipo_recurso,
            public_id=public_id,
            use_filename=False,
            unique_filename=False,
            overwrite=True,
        )
        return resultado.get("secure_url")
    except Exception as e:
        raise RuntimeError(f"Falló la subida a Cloudinary: {e}") from e
