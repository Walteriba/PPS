import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logging(app):
    """
    Configura un logger para consola y archivo rotativo.
    Los logs se guardarán en la carpeta 'logs'.
    """

    # Formato de los mensajes de log
    log_format = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s:%(lineno)d - %(message)s"
    )

    # Quitar los handlers por defecto de Flask
    app.logger.handlers.clear()

    # --- Handler para Consola ---
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    # --- Handler para Archivo (solo si no estamos en modo debug) ---
    if not app.debug:
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)

        log_file_path = os.path.join(log_dir, "vetlog.log")

        file_handler = RotatingFileHandler(
            log_file_path,
            maxBytes=1 * 1024 * 1024,
            backupCount=5,
        )
        file_handler.setFormatter(log_format)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    # Nivel general de logging
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
    app.logger.info("Logger configurado correctamente.")
