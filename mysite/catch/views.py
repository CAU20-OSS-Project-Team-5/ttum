from django.shortcuts import render
from PIL import Image

# Create your views here.

def catch(request):   # NL -> PlantUML -> Img file
  message = request.GET.get('message')
  text_file = open("Data/Output.txt", "w")
  text_file.write(message)
  text_file.close()

  im = Image.open("static/img/waterdog.jpg")
  im.save('static/img/UML.jpg')
  
  return render(request, 'catch.html', {'message': message, 'im': im})