import cv2
import pytesseract
import re
import numpy as np

def texto(imagen):
    global doc
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Configuración para Tesseract (usar idioma español)
    config = "--oem 3 --psm 6 -l spa"
    texto = pytesseract.image_to_string(imagen, config=config)

    # Dividir el texto extraído en líneas
    lineas = texto.splitlines()

    # Filtrar líneas vacías
    lineas = [linea for linea in lineas if linea.strip()]

    return lineas

# Función para mejorar la calidad de la imagen (filtros y ajuste de contraste)
def mejorar_imagen(gris):
    # Aplicar filtro de desenfoque para eliminar ruido
    gris = cv2.GaussianBlur(gris, (5, 5), 0)

    # Ajustar el contraste y brillo
    alpha = 1.5  # Contraste
    beta = 0     # Brillo
    mejorada = cv2.convertScaleAbs(gris, alpha=alpha, beta=beta)

    return mejorada