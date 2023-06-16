from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import logiserilazier,CustomUserSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

class register (GenericAPIView): 
    serilaizer = CustomUserSerializer

    def post (self , request):
        serilaizer = CustomUserSerializer(data=request.data)
        if serilaizer.is_valid():
            serilaizer.save()
            return Response(
                serilaizer.data, status = status.HTTP_201_CREATED
            )
        return Response(
            serilaizer.errors,status=status.HTTP_400_BAD_REQUEST
        )
# Create your views here.

class login (GenericAPIView):
    def post (self, request):
        data=request.data
        serializer = logiserilazier(data)
        email = data.get('email')
        password = data.get('password')
        user = serializer.login(email,password)
        user_instance = CustomUser.objects.get(email=email)
        serilaizer2 = CustomUserSerializer(user_instance)
        if  user : 
            return Response(
                serilaizer2.data , status = status.HTTP_200_OK
            )
        else :return Response(
            serializer.errors,status=status.HTTP_404_NOT_FOUND
        )


class loginview (GenericAPIView):
    def post (self, request):
        data = request.data
        usename = data.get('username')
        password = data.get('password')
        pass
