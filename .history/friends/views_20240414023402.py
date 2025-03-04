from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response

import jwt, datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from common_functions.common_function import getUser, getUserProfileForPosts
from users.models import User
from .models import FriendRequest, Friendship
from .serializers import FriendRequestSerializer, FriendshipSerializer
# Create your views here.
# friend_request.status = 'accepted'  # Cập nhật trạng thái của yêu cầu kết bạn thành 'accepted'
# friend_request.save()  # Lưu thay đổi vào cơ sở dữ liệu
# friend_request.delete()  # Xóa yêu cầu kết bạn khỏi cơ sở dữ liệu


class FriendsRequestsView(APIView):
    def get(self,request):
        user = getUser(request)
        
        if not user:
            return HttpResponseRedirect(reverse('users:login'))
        
        return render(request,'friends/friend.html')

class  SentFriendRequestView(APIView):
    def post(self, request, friend_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friend = User.objects.get(id=friend_id)
        except User.DoesNotExist:
            return Response({'error': 'Friend not found'}, status=404)
        
        existing_request = FriendRequest.objects.filter(from_id=user, to_id=friend).exists()
        
        if existing_request:
            return Response({'error': 'Friend request already sent'}, status=400)
        
        FriendRequest.objects.create(from_id=user, to_id=friend, status='pending')
        
        return Response({'success': 'Friend request sent successfully'})
    
class RevokeFriendRequestView(APIView):
    def post(self, request, friend_request_id):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friend_request_id = request.data.get('id')
            friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
            
            friend_request.delete()
            
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found'}, status=404)
        
        friend_request.delete()
        
        return Response({'success': 'Friend request revoked successfully'})
    
class AcceptFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        # print(request.data)
        
        try:
                friend_request_id = request.data.get('id')
                friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
                
                #friend_request.status = 'pending'
                friend_request.status = 'accepted'
                friend_request.save()
                
                friend_ship = Friendship.objects.create(
                user_id1 = user,
                user_id2 = friend_request.from_id                 
                )
                # Friendship.objects.all().delete()  
                friend_ship.save()     
                       
                return Response({'message': 'Friend request processed successfully'})
            
        except:
            return Response({'error': 'Error while saving friend request'}, status=400)

class DenineFriendRequestView(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        # print(request.data)
        
        try:
                friend_request_id = request.data.get('id')
                friend_request = get_object_or_404(FriendRequest, id = friend_request_id)
                
                #friend_request.status = 'pending'
                friend_request.status = 'denined'
                friend_request.save()  
                
                return Response({'message': 'Friend request processed successfully'})
            
        except:
            return Response({'error': 'Error while saving friend request'}, status=400)
    
class DeleteFriendShip(APIView):
    def post(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        try:
            friendship_id = request.get('id')
            friendship = get_object_or_404(Friendship, id = friendship_id)
            
            friendship.delete()
        except Friendship.DoesNotExist:
            return Response({'error': 'Friendship not found'}, status=404)
         
        return Response({'success': 'Friendship deleted successfully'})
    
class GetSentFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        list_friend_requests_sent = FriendRequest.objects.filter(from_id=user)
        print(list_friend_requests_sent)
        for friend_request_sent in list_friend_requests_sent:
            serializer = FriendRequestSerializer(friend_request_sent)
            print(serializer)
            
            friend_request = {
                "friend_request_sent" : serializer.data,
                "friend_request_profile": getUserProfileForPosts(friend_request_sent.to_id)
            }
            data.append(friend_request)
        return Response({
            "data" : data
        })

class  GetReceivedFriendRequestsView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        list_friend_requests_received = FriendRequest.objects.filter(to_id=user)
        print(list_friend_requests_received)
        for friend_request_received in list_friend_requests_received:
            serializer = FriendRequestSerializer(friend_request_received)
            print(serializer)
            
            friend_request = {
                "friend_request_received" : serializer.data,
                "friend_request_profile": getUserProfileForPosts(friend_request_received.from_id)
            }

            data.append(friend_request)

        return Response({
            "data": data
            })

class GetListFriendView(APIView):
    def get(self, request):
        user = getUser(request)
        
        if not user:
            return Response({'error': 'Unauthorized'}, status=401)
        
        data = []
        list_friend_ship = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
        print(list_friend_ship)
        
        
        for friend_ship in list_friend_ship:
             
            try:
                friend = {
                "friend_ship": FriendshipSerializer(friend_ship).data,
                "friend_profile": getUserProfileForPosts(friend_ship.user_id2) if user == friend_ship.user_id1 else getUserProfileForPosts(friend_ship.user_id1)
                }
                
                data.append(friend)
            except:
                return Response({'error': 'Friendship not found'}, status=404)
        return Response({
            "data": data
            })

class GetMutualFriendView(APIView):
        def get(self, request):
            user = getUser()
            if not user:
                return Response({'error': 'Unauthorized'}, status=401)
            
            friend_id = request.get('friend_id')    #lấy từ fe của các user
            
            friend = get_object_or_404(Friendship, id=friend_id)
            
            user_friendships = Friendship.objects.filter(Q(user_id1=user) | Q(user_id2=user))
            
            friend_friendships = Friendship.objects.filter(Q(user_id1=friend.user_id1) | Q(user_id2=friend.user_id2))
            
            mutual_friendships = user_friendships.intersection(friend_friendships)
            
            data = []
            
            for mutual_friendship in mutual_friendships:
                
                friend_profile = getUserProfileForPosts(mutual_friendship.user_id2) if user == mutual_friendship.user_id1 else getUserProfileForPosts(mutual_friendship.user_id1)
                
                data.append({
                "mutual_friendship": FriendshipSerializer(mutual_friendship).data,
                "friend_profile": friend_profile
                })
            
            return Response({
                "data": data
                })

class GetSuggestionFriendView():
        def get(self, request):
            print(request)