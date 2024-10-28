from django.urls import path 
from .views import *

urlpatterns = [
     path('', Home.as_view()),
     path('upload_images/', Load_data.as_view(), name="Upload_image"),
     path('tribunal/', lecturaCedula),

     
]
   