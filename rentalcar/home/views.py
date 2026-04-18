from django.shortcuts import render
from home.serializers import RegisterSerializers,BookingsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class Register(APIView):
    def post(self,request):
      serializer = RegisterSerializers(data=request.data)
      serializer.is_valid(raise_exception=True)
      serializer.save()

      return Response({"message":"User Registerd Succesfully "},status=status.HTTP_201_CREATED)
    

class Login(APIView):
   
   def post(self,request):

      username = request.data.get("username")
      password = request.data.get("password")

      user = authenticate(username=username, password=password)

      if user is None:
         return Response({"error":"invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
      
      token, created = Token.objects.get_or_create(user=user)

      return Response({
         "token":token.key
      })

class Booking(APIView):

   permission_classes = [IsAuthenticated]
   def post(self,request):
      serializer = BookingsSerializer(data=request.data,context={'request':request})
      serializer.is_valid(raise_exception=True)
      serializer.save()
      
      return Response(serializer.data,status=status.HTTP_201_CREATED)
   
class Home(APIView):
    def get(self,request):
       return Response("Hi this is only for ")
       