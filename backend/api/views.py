from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer

from .models import Task

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from uml_handler import UMLHandler

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
    return Response(serializer.data)

@api_view(['POST'])
def taskCreate(request):
    
    serializer = TaskSerializer(data=request.data)

    if Task.objects.last():
      task = Task.objects.last()  
      task.delete()

    if serializer.is_valid():
        serializer.save()

    task = Task.objects.last()
    uml_handler = UMLHandler(train_epoch=0)
    # Convert paragraph into usecase diagram image
    is_successful = uml_handler.convert_into_usecase_uml(task.title)

    # Update the usecase diagram image with user-updated PlantUML text
    is_successful = uml_handler.update_usecase_uml()

    task.title = 'converted!!'
    task.save() 

    return Response(serializer.data)

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


