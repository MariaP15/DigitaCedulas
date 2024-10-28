#Importaciones necesarias 
import cv2
import numpy as np
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from .lectura_id import *
from .CedulaP import *
import os

#Clase principal que invoca al html
class Home(View):
    def get(self, request):
        return render(request, 'index.html')


class Load_data(View):
    def post(self, request):
        # Capturar imagen enviada desde el frontend
        file = request.FILES.get('image')  # Obtener la imagen desde el formulario
        type = request.POST.get('type')
        if type == 'end':
            return JsonResponse({'datos':main()})
        if not file:
            return JsonResponse({'error': 'No se recibió ninguna imagen'}) #Mensaje de error en pantalla en caso de que la camara no cargue

        # Convertir la imagen a un formato que OpenCV pueda procesar
        fileread = file.read()
        np_array  = np.frombuffer(fileread, np.uint8)
        image = cv2.imdecode(np_array , cv2.IMREAD_GRAYSCALE)

        

        # Mejorar la imagen
        img_improved = mejorar_imagen(image)


        # Aplicar umbral adaptativo
        umbral = cv2.adaptiveThreshold(img_improved, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 55, 25)

        # Escalar la imagen
        height, width = umbral.shape
        img_resized = cv2.resize(umbral, (width * 2, height * 2))

        # Extraer texto usando Tesseract
        lineas = texto(img_resized)

        # Crear un diccionario con los datos extraídos
        
        if type == 'front':
            datos = {
            'cedula': lineas[2] if len(lineas) > 2 else '',
            'nombre': lineas[5] if len(lineas) > 5 else '',
            'apellido1': lineas[6] if len(lineas) > 6 else '',
            'apellido2': lineas[7] if len(lineas) > 7 else '',
            }
        elif type == 'end':
            return JsonResponse({'datos':main()})
        else:

            datos = {
            'cedula': lineas[1] if len(lineas) > 1 else '',
            'fecha_nacimiento': lineas[2] if len(lineas) > 2 else '',
            'lugar_nacimiento': lineas[3] if len(lineas) > 3 else '',
            'domicilio_electoral': lineas[4] if len(lineas) > 4 else '',
            'nombre_padre': lineas[5] if len(lineas) > 5 else '',
            'nombre_madre': lineas[6] if len(lineas) > 6 else '',
            'vencimiento': lineas[7] if len(lineas) > 7 else '',
        }
        return JsonResponse({'datos': datos})
    

from django.http import JsonResponse, HttpResponse

def lecturaCedula(request):
    if request.method == 'POST':
        cedula = request.POST.get('cedula')
        if not cedula:
            return JsonResponse({'error': 'No se proporcionó un número de cédula'}, status=400)

        data_file = r"C:\Users\maria\Downloads\Proyectos\QRCedulas\Cedulas\PADRON_COMPLETO.txt"

        try:
            # Lee el archivo línea por línea
            with open(data_file) as data_obj:
                id_lines = data_obj.readlines()

            # Procesa cada línea
            for line in id_lines:
                fields = line.split(',')
                id = fields[0].strip()

                if str(id) == str(cedula):
                    canton = fields[1].strip()
                    expiration = fields[3].strip()
                    name = fields[5].strip().title()
                    surname1 = fields[6].strip().title()
                    surname2 = fields[7].strip().title()

                    # Formatea la fecha de vencimiento a DD/MM/AAAA
                    day = expiration[6:8]
                    month = expiration[4:6]
                    year = expiration[0:4]
                    formatted_date = f"{day}/{month}/{year}"

                    # Datos formateados
                    datos = {
                        "Cedula": id,
                        "Nombre": name,
                        "Apellido1": surname1,
                        "Apellido2": surname2,
                        "Canton": canton,
                        "Vencimiento": formatted_date
                    }

                    # Retorna los datos en formato JSON
                    return JsonResponse(datos, status=200)

            # Si no se encontró la cédula
            return JsonResponse({'error': 'Cédula no encontrada'}, status=404)

        except FileNotFoundError:
            return JsonResponse({'error': 'Archivo de datos no encontrado'}, status=500)

    # Si no es una solicitud POST
    return JsonResponse({'error': 'Método no permitido'}, status=405)



