# chat/views.py
from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from common_functions.common_function import getUser, getUserProfileForPosts
from users.models import User
from userprofiles.models import UserProfile

from django.db.models import Q
from .serializers import UserInfoSerializer, ImageSerializer
from rest_framework import generics

class navbarView(APIView):     
    def navbar(request):
        return render(request, "navbar/navbar.html")


class SearchListView(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()

    def post(self, request):
        print(request.data)
        # username = self.request.query_params.get('username', '')
        # print("hhi + {username}")
        # users =  UserProfile.objects.filter(
        #     Q(user_id__email__icontains=username) |
        #     Q(first_name__icontains=username) |
        #     Q(last_name__icontains=username)
        # )
        # #print(users)
        # if not users.exists():
        #     return Response({"detail": "Không tìm thấy người dùng"})
        
        #serializer = UserInfoSerializer(users)
        return Response(serializer.data)
    
    

    



    