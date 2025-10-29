from io import BytesIO
import requests
from flask import current_app
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def crear_pdf_historia_clinica(paciente, tutor, consultas):
    """
    Crea un PDF con la historia clínica a partir de los objetos de datos.
    Devuelve un buffer de BytesIO con el PDF generado.
    """
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    # --- Cabecera del PDF ---
    p.setFont("Helvetica-Bold", 18)
    p.drawString(50, y, f"Historia Clínica: {paciente.nombre}")
    y -= 30

    # Lógica para la imagen del paciente
    imagen_path = paciente.imagen
    try:
        if imagen_path and imagen_path.startswith('http'):
            response = requests.get(imagen_path, stream=True)
            response.raise_for_status()
            p.drawImage(BytesIO(response.content), width - 150, y - 60, width=100, height=100, preserveAspectRatio=True, mask='auto')
        elif imagen_path:
            full_path = os.path.join(current_app.root_path, imagen_path.strip('/'))
            if os.path.exists(full_path):
                p.drawImage(full_path, width - 150, y - 60, width=100, height=100, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"Error al cargar la imagen: {e}")

    # Datos del Paciente y Tutor
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Datos del Paciente")
    p.setFont("Helvetica", 10)
    y -= 15
    p.drawString(55, y, f"Especie: {paciente.especie} | Raza: {paciente.raza} | Sexo: {paciente.sexo}")
    y -= 15
    p.drawString(55, y, f"Fecha de Nacimiento: {paciente.fecha_nacimiento.strftime('%d/%m/%Y')}")
    y -= 25
    p.setFont("Helvetica-Bold", 11)
    p.drawString(50, y, "Datos del Tutor")
    p.setFont("Helvetica", 10)
    y -= 15
    p.drawString(55, y, f"Nombre: {tutor.nombre} {tutor.apellido}")
    y -= 15
    p.drawString(55, y, f"Teléfono: {tutor.telefono}")
    y -= 25
    p.line(50, y, width - 50, y)
    y -= 20
    
    # --- Contenido de las consultas ---
    if not consultas:
        p.drawString(50, y, "No se encontraron consultas para este paciente.")
    else:
        for consulta in consultas:
            if y < 120:
                p.showPage()
                y = height - 70
            p.setFont("Helvetica-Bold", 12)
            p.drawString(60, y, f"Fecha: {consulta.fecha.strftime('%d/%m/%Y')}")
            y -= 20
            p.setFont("Helvetica", 10)
            p.drawString(70, y, f"Anamnesis: {consulta.anamnesis or 'N/A'}")
            y -= 15
            p.drawString(70, y, f"Diagnóstico: {consulta.diagnostico or 'N/A'}")
            y -= 15
            p.drawString(70, y, f"Tratamiento: {consulta.tratamiento or 'N/A'}")
            y -= 25

    p.save()
    buffer.seek(0)
    return buffer
            