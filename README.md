# Digitalizacion de Cedulas

## Requerimientos
Descargar el Padron Completo del Tribunal Supremo de elecciones 'https://www.tse.go.cr/descarga_padron.htm'


## Instalacion de python 

Se debe instalar el archivo ejecutable desde internet
Con el siguiente url se descargara la version compatible con el programa 'https://www.python.org/downloads/release/python-3117/'

Abre la carpeta del proyecto y desde la ruta del proyecto se debe ejecutar una terminal
Seguidamente se creara el entorno virtual del proyecto
```
  $ python -m venv venv 
```
Una vez instalado el entorno virtual este se debera activar
```
$ .\venv\Scripts\activate
```

Se deben instalar los siguientes requerimientos 
```
$ pip install -r requirements.txt
```

Por ultimo se debe ejecutar el proyecto
```
$ python manage.py runserver
```

# Como digitalizar 
Despues de ingresar al link de la pagina, se necesita otorgarle permisos de uso a la camara

- Seguidamente deberas poner el documento de identidad en el recuadro de la camara, centrado y lo mas nitido posible, luego presiona el boton de "Escanear"
Una vez presionado el boton, la pagina desplegara un card con toda la informacion obtenida

Para recargar la pagina toca el boton de la esquina superior derecha, llamado "Limpiar Pantalla
"



