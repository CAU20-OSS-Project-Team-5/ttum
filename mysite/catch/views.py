from django.shortcuts import render
from PIL import Image
import numpy as np

# Create your views here.

def catch(request):   # NL -> PlantUML -> Img file
  message = request.GET.get('message')
  text_file = open("Data/Output.txt", "w")
  text_file.write(message)
  text_file.close()

  img_url = "../static/img/waterdog.jpg"
  
  return render(request, 'catch.html', {'message': message, 'img_url': img_url})