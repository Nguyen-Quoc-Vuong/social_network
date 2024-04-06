from .serializers import UserSerializer
from .models import User
from userprofiles.views import SetUserProfileView, SetImageProfileView

import jwt, datetime
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ValidationError

# Create your views here.
class LoginView(APIView):
    def makeToken(self, user):
        payload = {
            'id': user.id,
            'exp': datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.now(datetime.UTC)
        }

        token = jwt.encode(payload=payload, key='secret', algorithm='HS256')
        
        return token
    
    def get(self, request):
        reponse = render(request, 'users/login.html')
        print(request.COOKIES.get('jwt'))
        
        reponse.delete_cookie('jwt')
        
        return reponse
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({'warning': 'User not found!'})

        if not user.check_password(password):
            return Response({'warning': 'Incorrect password!'})
        
        user.set_last_login()
        
        token = self.makeToken(user)
        
        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'success': 'Login success!!!',
            'jwt': token,
            'redirect_url': '/userprofiles/' + f"?id={user.id}"
        }
        
        return response
  
class RegisterView(APIView):
    def get(self, request):
        
        response = render(request, 'users/register.html')
        print(request.COOKIES.get('jwt'))
        response.delete_cookie('jwt')
        
        return response
            
    def post(self, request):
        # print(request.data)
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()
                
                SetUserProfileView().post(request, user)
                SetImageProfileView().post(request, user)
                
                # user.set_last_login()
                
                token = LoginView().makeToken(user)
                
                response = Response()
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    'success': 'Register success!!! Welcome to the feisubukku!',
                    'jwt': token,
                    'redirect_url': '/userprofiles/' + f"?id={user.id}"
                }
                
                return response
            
        except ValidationError as e:
            if e.detail.get('email'):
                return Response({'warning': e.detail.get('email')})
            if e.detail.get('comfirm_password'):
                return Response({'warning': e.detail.get('comfirm_password')})
            if e.detail.get('check_password'):
                return Response({'warning': e.detail.get('check_password')})
        except Exception as e:
            return Response({'error': 'Something went wrong. Please try again.'})

class LogoutView(APIView):
    def post(self, request):
        response = HttpResponseRedirect(reverse('users:login'))
        response.delete_cookie('jwt')
        response.data = {
            'message': 'logout success'
        }
        return response