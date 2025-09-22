from utils.cloudinary_utils import subir_y_obtener_url

if __name__ == "__main__":
    # Cambia la ruta por una imagen real que tengas en tu PC
    ruta_archivo = "static/imgs/default-avatar.jpg"
    identificador = "prueba_cloudinary_avatar"

    try:
        url = subir_y_obtener_url(ruta_archivo, identificador)
        if url:
            print(f"¡Éxito! Imagen subida a Cloudinary.")
            print(f"URL pública: {url}")
        else:
            print("La subida falló. Revisa la configuración y la ruta del archivo.")
    except Exception as e:
        print(f"Error detallado: {e}")
