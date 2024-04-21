from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt 

from users.models import User
from users.serializers import UserSerializer

from .models import UserProfile, ImageProfile, Image
from .serializers import UserProfileSerializer, ImageProfileSerializer
from .forms import ImageProfileForm

from posts.models import Posts, MediaOfPosts
from posts.serializers import PostsSerializer, MediaOfPostsSerializer

from posts.views import CreatePostsAfterSetMediaProfileView

# from users.views import LoginView

from common_functions.common_function import getUser, getTimeDuration, getUserProfileForPosts

import time

class ProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/profile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:profile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

def main_view(request):
        obj = Image.objects.get(pk=1)
        context = {'obj': obj}  
        return render(request, 'userprofiles:editImages', context)

class EditImages(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)                    
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/editImages.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editImages') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
    
class EditProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401)
            return render(request, 'userprofiles/editProfile.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editProfile') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

class EditStoryView(APIView):
    def get(self, request):
        user = getUser(request)
        print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            if int(request.query_params.get('id')) != user.id:
                return Response({'error': 'Unauthorized'}, status=401) 
            return render(request, 'userprofiles/editStory.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:editStory') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)
    def post(self, request):
        print(request.data)
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.save()

                SetUserProfileView().post(request, user)

                return Response({'success': 'Update success'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)

        #         token = LoginView().makeToken(user)

        #         response = Response()
        #         response.set_cookie(key='jwt', value=token, httponly=True)
        #         response.data = {
        #             'success': 'Your story has been successfully updated!!!',
        #             'jwt': token,
        #             'redirect_url': '/userprofiles/' + f"?id={user.id}"
        #         }
                
        #         return response
        # except Exception:
        #     return Response({'error': 'Sonething went wrong. Please try again.'})

class ListFriendsView(APIView):
    def get(self, request):
        user = getUser(request)
        # print(user)
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        if request.query_params.get('id'):
            return render(request, 'userprofiles/listFriends.html')
        
        id_requested = request.query_params.get('id') or user.id
        
        path = reverse('userprofiles:listFriends') + '?id=' + str(id_requested)
        
        return HttpResponseRedirect(path)

class GetProfileView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return Response({'error': 'Unauthorized'}, status=401)

        # print(request.query_params.get('id'))
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id
        
        try:
            context = self.getProfile(idUserRequested)
        except Exception as e:
            return Response({'error': str(e)}, status=404)
        
        context['isOwner'] = True if user.id == idUserRequested else False
                
        return Response(context)
    
    def getProfile(self, id):
        try:
            user = User.objects.get(id=id)
            userprofile = UserProfile.objects.get(user_id=id)
            imageprofile = ImageProfile.objects.get(user_id=id)
            
            context = {
                'user': UserSerializer(user).data,
                'userprofile': UserProfileSerializer(userprofile).data,
                'imageprofile': ImageProfileSerializer(imageprofile).data
            }
            
            return context
        except Exception as e:
            raise e
    
       
class SetUserProfileView(APIView):
    # update user profile
    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))
        
        user.email = request.data.get('email')

        userprofile = UserProfile.objects.filter(user_id=user).first()

        if userprofile:
            userprofile.first_name = request.data.get('first_name')
            userprofile.last_name = request.data.get('last_name')
            userprofile.gender = request.data.get('gender')
            userprofile.birth_date = request.data.get('birth_date')
            userprofile.phone = request.data.get('phone')
            userprofile.bio = request.data.get('bio') or None
            userprofile.address = request.data.get('address') or None
            userprofile.school = request.data.get('school') or None
            userprofile.work = request.data.get('work') or None

            userprofile.save()

        return HttpResponseRedirect(reverse('userprofiles:profile'))
    
    # create a new user profile
    def post(self, request, user):
        userprofile = UserProfile.objects.create(   user_id=user,
                                                    first_name=request.data.get('first_name'),
                                                    last_name=request.data.get('last_name'),
                                                    gender=request.data.get('gender'),
                                                    phone=request.data.get('phone'),
                                                    birth_date=request.data.get('birth_date') or None,
                                                )

        userprofile.save()

        return Response({'message': 'User profile created successfully!'})
class SetImageProfileView(APIView):
    # update user profile
    def post(self, request):
        user = getUser(request)
        
        if not isinstance(user, User):
            return HttpResponseRedirect(reverse('users:login'))

        imageprofile = ImageProfile.objects.filter(user_id=user).first()

        if imageprofile:
            imageprofile.avatar = request.FILES['avatar'] or None
            imageprofile.background = request.FILES['background'] or None
            imageprofile.save()
            
            if imageprofile.avatar:
                CreatePostsAfterSetMediaProfileView().createAvatarPosts(user, imageprofile.avatar)
            
            if imageprofile.background:
                CreatePostsAfterSetMediaProfileView().createBackgroundPosts(user, imageprofile.background)

        return HttpResponseRedirect(reverse('userprofiles:profile'))
    
    def post(self, request, user):
        imageProfileForm = ImageProfileForm(request.POST or None, request.FILES or None)
        if imageProfileForm.is_valid():
            imageProfileForm.save(user)
            
            if imageProfileForm.cleaned_data.get('avatar'):
                CreatePostsAfterSetMediaProfileView().createAvatarPosts(user, imageProfileForm.cleaned_data.get('avatar'))
              
            if imageProfileForm.cleaned_data.get('background'):
                CreatePostsAfterSetMediaProfileView().createBackgroundPosts(user, imageProfileForm.cleaned_data.get('background'))
                  
        return Response({'message': 'Image profile created successfully!'})
class GetPostsView(APIView):
    def get(self, request):
        
        start_time = time.time()
        
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        
        # print(request.query_params.get('id'))
        
        if request.query_params.get('id'):
            idUserRequested = int(request.query_params.get('id'))
        else:  
            idUserRequested = user.id

        userRequest = User.objects.filter(id=idUserRequested).first()
        
        if not userRequest:
            return Response({'error': 'User not found'}, status=404)
        
        userDataForPosts = getUserProfileForPosts(userRequest)
        
        posts = Posts.objects.filter(user_id=userRequest).prefetch_related('mediaofposts_set').order_by('-created_at')[:10] 
        
        for post in posts:
            posts_data = PostsSerializer(post).data
            media_data = MediaOfPostsSerializer(post.mediaofposts_set.all(), many=True).data
            
            posts_data['media'] = media_data
            posts_data['user'] = userDataForPosts

            posts_data['created_at'] = getTimeDuration(post.created_at)
        
            data.append(posts_data)
            
        reponse = Response()
        
        reponse.data = {
            'posts': data,
            'isOwner': True if user.id == idUserRequested else False
        }
        
        end_time = time.time()  # lưu thời gian kết thúc

        execution_time = end_time - start_time  # tính thời gian thực thi

        print(f"The function took {execution_time} seconds to complete")

        return reponse
    
class GetUserProfileBasicView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        userprofile = UserProfile.objects.filter(user_id=user).first()
        imageprofile = ImageProfile.objects.filter(user_id=user).first()
        
        profileSerializer = UserProfileSerializer(userprofile)
        imageSerializer = ImageProfileSerializer(imageprofile)
        
        context = {
            'user_id': user.id,
            'name': f"{profileSerializer.data.get('first_name')} {profileSerializer.data.get('last_name')}",
            'avatar': imageSerializer.data.get('avatar')
        }
        
        return Response(context)