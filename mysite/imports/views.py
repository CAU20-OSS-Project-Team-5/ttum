from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import json

def index(request):
  return render(request, 'index.html')

def throw(request):
  return render(request, 'index.html')





