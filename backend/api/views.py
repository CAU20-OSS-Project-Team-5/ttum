from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from .models import Task

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from backend.nlp.uml_handler import UMLHandler
import uuid


# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/task-list',
        'Detail View':'/task-detail/<str:pk>/',
        'Create':'/task-create/',

        'Update':'/task-update/<str:pk>/',
        'Delete':'/task-delete/<str:pk>/',
    }

    return Response(api_urls)

@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
    tasks = Task.objects.get(id=pk)
    serializer = TaskSerializer(tasks, many=False)
    return Response(tasks.title)

@api_view(['POST'])
def taskCreate(request):
    
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():   # 데이터 Database의 api_task table에 저장
        serializer.save()

    task = Task.objects.last()  # 방금 추가한 데이터를 불러옴
    
    uml_handler = UMLHandler(train_epoch=0)
    
    if task._type == "0":
        # Create hash code
        hash = uuid.uuid4().hex
        hashed_plantuml_file_name = str(hash) + '.plantuml'
        hashed_image_file_name = str(hash) + '.png'
        print("Hashed file name: " + hashed_plantuml_file_name)
        # Convert paragraph into usecase diagram image

        is_successful = uml_handler.convert_into_usecase_uml(task.title, usecase_file_name=hashed_plantuml_file_name)
        url = os.path.join('.','media','texts',hashed_plantuml_file_name)
        task.title = ""
        with open(url, "r") as f:
            lines = f.readlines()
            for line in lines:
                task.title += line

        task.image_name = str(hash)
        task.images = os.path.join('..','media','diagrams',hashed_image_file_name)
    if task._type == "1":
        # Update the usecase diagram image with user-updated PlantUML text
        text = open(os.path.join('.','media','texts', task.image_name + '.plantuml'), 'w')
        
        text.write(task.title)
        text.close()
        
        file_plantuml = task.image_name + '.plantuml'
        
        is_successful = uml_handler.update_usecase_uml(usecase_file_name=file_plantuml)

        file_image =  task.image_name + '.png'
        
        task.images = os.path.join('..','media','diagrams',file_image)

    
    print("Done updating the image with the new PlantUML text file.")
    
    task.save()
    
    if task._type == "0":
        if Task.objects.first():
            task = Task.objects.first()
            # Cleanup usecase diagram images and texts from 'media/'
            uml_handler.cleanup_plantuml_files(plantuml_text_file_name=task.image_name)
            task.delete()
    if task._type == "1":
        if Task.objects.first():
            task = Task.objects.first()
            task.delete()
    
    return Response(serializer.data)

@api_view(['GET'])
def viewImage(request, pk):
    task = Task.objects.get(id=pk)
    #serializer = TaskSerializer(instance=task, data=request.data)

    return Response(task.images)

@api_view(['POST'])
def taskUpdate(request, pk):
    task = Task.objects.get(id=pk)
    serializer = TaskSerializer(instance=task, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def taskDelete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()

    return Response('Item successfully delete!')


