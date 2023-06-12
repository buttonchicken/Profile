from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from .serializers import *
import os
from .constants import *

# Create your views here.

class Register(APIView):
    def post(self,request):
        try:
            data = request.data
            username = data['username']
            password = data['password']
        except KeyError:
            return Response({'message':'Please enter the username and password !!'},status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists(): #checking if user already exists
            return Response({'success': False, "message": "Username already taken !!"},status=status.HTTP_400_BAD_REQUEST)
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_object = User()
        user_object.username=username
        user_object.set_password(password)
        user_object.save()        
        refresh = RefreshToken.for_user(user_object)
        return Response({"success": True, "message": "Your account has been successfully activated!!",
                'payload': serializer.data,
                'refresh': str(refresh),
                'access': str(refresh.access_token)},
                status=status.HTTP_202_ACCEPTED)

class Login(APIView):
    def post(self,request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response({'message':'Please enter all the details !!'},status=status.HTTP_400_BAD_REQUEST)
        user=authenticate(username=username,password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            serializer = RegisterSerializer(user)
            return Response({"success": True, "message": "Login successful",
                            'payload': serializer.data,
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)},
                            status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'message':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)

class UpdateProfile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def patch(self,request):
        user = request.user
        serializer = UpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                existing_path = user.profile_picture.path
                if os.path.exists(existing_path) and 'profile_picture' in request.data.keys():
                    os.remove(existing_path)
            except:
                pass
            serializer.save()
            serialized_data = DisplaySerializer(user).data
            return Response({'message':'Profile updated successfully', 'payload':serialized_data}, status=status.HTTP_202_ACCEPTED)
        return Response({'message':'Invalid data'},status=status.HTTP_400_BAD_REQUEST)
        