from django.shortcuts import render
from rest_framework.response import Response
# from rentalcar.templates import index.html



def home(request):
    return Response("Hi this is for sample testing")