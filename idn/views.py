#Importaciones necesarias 
import cv2
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .lectura_id import *


#Clase principal que invoca al html
class Home(View):
    def get(self, request):
        return render(request, 'index.html')


class Load_data(View):
    def post(self, request):
        # Capturar imagen enviada desde el frontend
        file = request.FILES.get('image')  # Obtener la imagen desde el formulario
        if not file:
            return JsonResponse({'error': 'No se recibió ninguna imagen'}) #Mensaje de error en pantalla en caso de que la camara no cargue

        # Convertir la imagen a un formato que OpenCV pueda procesar
        image_array = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        # Convertir a escala de grises
        gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Redimensionar la imagen para mejorar la precisión del OCR
        altura, anchura = gris.shape
        resized_image = cv2.resize(gris, (anchura * 4, altura * 4), interpolation=cv2.INTER_LINEAR)

        # Mejorar la imagen
        img_improved = mejorar_imagen(resized_image)

        # Aplicar umbral adaptativo
        umbral = cv2.adaptiveThreshold(img_improved, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

        # Extraer texto usando Tesseract
        lineas = texto(umbral)

        # Crear un diccionario con los datos extraídos
        datos = {
            'cedula': lineas[1] if len(lineas) > 1 else '',
            'nombre': lineas[2] if len(lineas) > 2 else '',
            'apellido1': lineas[3] if len(lineas) > 3 else '',
            'apellido2': lineas[4] if len(lineas) > 4 else '',
            'fecha_nacimiento': lineas[5] if len(lineas) > 5 else '',
            'lugar_nacimiento': lineas[6] if len(lineas) > 6 else '',
            'domicilio_electoral': lineas[7] if len(lineas) > 7 else '',
            'nombre_padre': lineas[8] if len(lineas) > 8 else '',
            'nombre_madre': lineas[9] if len(lineas) > 9 else '',
            'vencimiento': lineas[10] if len(lineas) > 10 else '',
        }

        return JsonResponse({'datos': datos})
