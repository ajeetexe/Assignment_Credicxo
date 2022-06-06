from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate,login
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.

class SignupApi(APIView):
    def post(self,request,format=None):
        serializer = UserSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message':'Succesfully Created'}, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_404_NOT_FOUND)


class LoginApi(APIView):
    def post(self,request,format=None):
        data = request.data
        if data.get('username') is None or data.get('password') is None:
            return Response(status=status.HTTP_404_NOT_FOUND,data="Username or password is not found")
        
        user = User.objects.filter(username = data.get('username')).first()
        if user is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED,data="Invalid Username")
        
        user_obj = authenticate(username = data.get('username'),password=data.get('password'))
        if user_obj:
            login(request,user_obj)
            return Response(status=status.HTTP_200_OK,data='Welcome')
        else:
            return Response(status=status.HTTP_403_FORBIDDEN,data='Invalid Password')

class ForgetPasswordApi(APIView):
    pass


class AddUserAndListViewApi(APIView):
    # permission_classes = []
    def get(self,request,format=None):
        group = Group.objects.get_or_create(name="credicxo")
        print(request.user)
        if request.user.is_superuser:
            users = User.objects.all()
            if users:
                for x in users:
                    group.user_set.add(x)
                    print(x)
        elif request.user.is_staff:
            users = User.objects.filter(is_staff=False,is_supperuser=False).all()
            if users:
                for x in users:
                    group.user_set.add(x)
        return Response(data={"Success"},status=status.HTTP_200_OK)
