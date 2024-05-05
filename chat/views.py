import datetime
import logging
import json
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.db.models import Subquery, OuterRef, Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from social_network.redis_conn import redis_server

from .serializers import MessageSerializer, UserInfoSerializer, ConversationSerializer, ChannelSerializer, MesseejiSerializer

from users.models import User
from userprofiles.models import UserProfile

from .models import Conversation, Message, Channel, Messeeji, UserMess, Participants

from common_functions.common_function import getUserProfileForPosts, getTimeDuration, getUser
from django.shortcuts import render, redirect
from mongoengine.errors import DoesNotExist
logger=logging.getLogger(__name__)

class MesseejiView():
    pass 

class ChatTestView(APIView):

    def post(self, request):
        try:
            username = request.POST.get('username')
            print('post called')
            print(username)
            list_users = SearchUser.search(SearchUser, username)
            print("list users:", list_users)
            user_ids = [user.user_id.id for user in list_users]
            print(user_ids)
            list_channels = Channel.objects(user_id__in=user_ids)
            print(list_channels)
            
            return render(request, "chat/index.html")
        
        except Channel.DoesNotExist:
            logger.exception("Channel does not exist")
            CreateChannel.create(request)

    def showAllChannel(request, list_channels):
        response = Response()

        data = []
        for channel in list_channels:
            data.append(ChannelSerializer(channel).data)
        
        response.data = {
            'channel' : data
        }
        return response

    def get(self, request):
        context = {}
        return render(request, "chat/index.html", context)

class GetMesseeji(APIView):
    def post(self, request):
        try:
            channel_id = request.data.get('channel_id')
            if (redis_server.get(f'chat_{channel_id}')):
                all_messeeji = redis_server.get(f'chat_{channel_id}')
            else:    
                all_messeeji = Messeeji.objects(channel_id=channel_id)
                redis_server.set(f'chat_{channel_id}', all_messeeji)
            response = Response()
            data = []
            
            if not all_messeeji:
                response.data = {
                    "status" : "no messeeji found!",
                    "data" : []
                }
            else:
                for messeeji in all_messeeji:
                    messeeji_data = MesseejiSerializer(messeeji).data
                    data.append(messeeji_data)
                response.data = {
                    'status' : "messeeji found! bandai",
                    'data' : data
                }
            return response
        except Exception as e:
            logger.exception(f"Error fetching messeeji: {str(e)}")

class GetChannels(APIView):
    def get_channels_by(query):
        channels = Channel.objects(query)
        
        list_channels = []
        for c in channels:
            list_channels.append(ChannelSerializer(c))
        return list_channels

    def get(self, request):
        response = Response()
        try:
            channel_id = int(request.data.get('post_id'))
            list_channels = self.get_channels_by(__raw__={'channel_id':channel_id})

            response.data = {
                'channel' : list_channels
            }
        except Exception as e:
            logger.exception(f"Error fetching channels: {str(e)}")
        return response
    
class CreateMesseeji(APIView):
    def create(self, request):
        return Messeeji(
            sender_id=int(request.data.get('user_id')),
            channel_id=request.data.get('channel_id'),
            message_content=request.data.get('message_content'),
            status=request.data.get('status'),
            created_at=datetime.datetime.now(),
        )

    def post(self, request):
        try:
            user = getUser(request)
            if not user:
                return Response({"message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)
            
            response = Response()

            messeeji = self.create(request)
            messeeji.save()
            logger.info('messeeji created successfully')
            response.data = {
                "status": "new messeeji created!",
                "data": [MesseejiSerializer(messeeji).data]
            }
            return response
        except Exception as e:
            logger.exception(f"Error creating messeeji: {str(e)}")

class CreateChannel(APIView):
    def check_existing_channel(self, user_id1, user_id2):
        try:
            part_user1 = Participants.objects(user_id=user_id1)
            part_user2 = Participants.objects(user_id=user_id2)
            channels_user1 = [participant.channel_id for participant in part_user1]
            channels_user2 = [participant.channel_id for participant in part_user2]
            common_channels = set(channels_user1) & set(channels_user2)
            if common_channels:
                channel = Channel.objects(channel_id=list(common_channels)[0])
                return True, channel
            else:
                return False, None
        except DoesNotExist:
            logger.error("Failed to check existing channel: %s", str(e))
            return False, None

    def create(self, request):
        try: 
            user = getUser(request)
            user_id = user.id
            target_id = request.data.get('target_id')
            existed_channel = self.check_existing_channel(user_id, target_id)
            if existed_channel[0]:
                output_channel = existed_channel[1].first()
                return False, output_channel
            else:
                new_channel =  Channel(
                    created_at = datetime.datetime.now(),
                    capacity = 2,
                )
                part_user = Participants(
                    user_id = user_id,
                    channel_id = new_channel.id,
                )
                part_target = Participants(
                    user_id = target_id,
                    channel_id = new_channel.id
                )
                new_channel.save()
                part_user.save()
                part_target.save()
                logger.info("New channel created between users: %s and %s", user_id, target_id)
            return True, new_channel
        except Exception as e:
            logger.error("Failed to create channel: %s", str(e))
            return False, None
    
    def post(self, request):
        try:
            user = getUser(request)
            if not user:
                return Response({"message": "Unauthorized"}, status=401)
            
            response = Response()
            success, channel = self.create(request)
            if not channel:
                response.data = {
                    "status" : "no channel created!",
                    "data" : []
                }
            else:
                output_channel = channel

            if success:
                response.data = {
                    "status" : "new channel created!",
                    "data" : [ChannelSerializer(output_channel).data]
                }
            else:
                response.data = {
                    "status" : "existing channel found!",
                    "data" : [ChannelSerializer(output_channel).data]
                }
            return response
        except Exception as e:
            logger.exception(f"Error creating channel: {str(e)}")


class CreateConversationView(APIView):
    def createConversation(self, request):
        try:
            conversation = Conversation.objects.create(
                conversation_id = 1,
                title = request.data.get('title') or None,
                status='visible'
            )
            conversation.save()
            logger.info('created conversation successfully')
        except:
            logger.error('error when creating Conversation')
            return Response({'error':'error when creating Conversation'})
        return conversation
    def post(self, request):
        conversation = self.createConversation(request)
        data = []

        conversation_data = ConversationSerializer(conversation).data

        data.append(conversation_data)

        return Response({'success': 'Conversation created!',
                         'conversation': data})

class CreateConversationView(APIView):
    def createConversation(self, request):
        try:
            conversation = Conversation.objects.create(
                conversation_id = 1,
                title = request.data.get('title') or None,
                status='visible'
            )
            conversation.save()
            logger.info('created conversation successfully')
        except Exception as e:
            logger.error(f"Error creating conversation: {e}")
            return None
        return conversation
    
    def post(self, request):
        conversation = self.createConversation(request)
        if conversation:
            data = [ConversationSerializer(conversation).data]
            return Response({'success': 'Conversation created!', 'conversation': data})
        else:
            return Response({'error':'Error when creating Conversation'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ConversationView(APIView):
    serializer_class = ConversationSerializer

    def get(self, request):
        response = Response()
        try:
            user = getUser(request)
            convs = Conversation.objects.filter(
                Q(conv__sender=user) | Q(conv__receiver=user)
            ).distinct()
            data = []
            for conv in convs:
                conv_data = ConversationSerializer(conv).data
                data.append(conv_data)

            response.data = {
                "conversations" : data
            }
        except Exception as e:
            logger.error(f"Error fetching conversations: {e}")
        return response

class MessageView(generics.ListAPIView):
    
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create_init_message(self, request):
        try:
            conversation_id = request.data.get('conversation_id')
            sender_id = request.data.get('sender_id')
            receiver_id = request.data.get('receiver_id')
            content = ""

            # Validate input data
            if not all([conversation_id, sender_id, receiver_id, content]):
                return Response({"error": "Missing required fields"}, status=400)

            # Create the message
            message = Message.objects.create(
                conversation_id=conversation_id,
                user_id=request.user.id,
                sender_id=sender_id,
                receiver_id=receiver_id,
                content=content,
                is_read=False  # Assuming the message is initially unread
            )

            # Serialize the message data
            serializer = MessageSerializer(message)

            return Response(serializer.data, status=201)
        except Exception as e:
            logger.error(f"Error creating initial message: {e}")
            return Response({"error": "Error creating initial message"}, status=500)

    def get_queryset(self):
        try:
            user_id = self.kwargs['user_id']
            
            messages = Message.objects.filter(
                id__in = Subquery(
                    User.objects.filter(
                        Q(sender__receiver=user_id),
                        Q(receiver__sender=user_id),
                    ).distinct().annotate(
                        last_message = Subquery(
                            Message.objects.filter(
                                Q(sender=OuterRef('id'), receiver=user_id),
                                Q(receiver=OuterRef('id'), sender=user_id),
                            ).order_by("-id")[:1].values_list("id", flat = True)
                        )
                    ).values_list("last_message", flat=True).order_by("-id")
                )            
            ).order_by("-id")

            return messages
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")

class GetMessages(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            sender_id = self.kwargs['sender_id']
            receiver_id = self.kwargs['receiver_id']

            messages = Message.objects.filter(
                sender__in=[sender_id, receiver_id],
                receiver__in=[sender_id, receiver_id],
            )

            return messages
        except Exception as e:
            logger.error(f"Error fetching messages: {e}")

class SendMessage(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class ProfileDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()
    permission_classes = [IsAuthenticated]

class SearchUser(generics.ListAPIView):
    serializer_class = UserInfoSerializer
    queryset = UserProfile.objects.all()
    # permission_classes = [IsAuthenticated]

    def search(self, username):
        users = []
        if(username != '@'):
            users = UserProfile.objects.filter(
                Q(user_id__email__icontains=username) |
                Q(first_name__icontains=username) |
                Q(last_name__icontains=username) 
            )
        else:
            users = UserProfile.objects.filter()
        return users

    def list(self, request, *args, **kwargs):
        try:
            username = self.kwargs['username']
            users = self.search(username)
            current_user_id = getUser(request).id
            users = [user for user in users if user.id != current_user_id]
            if not users:
                return Response(
                    {"detail" : "No user found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = UserInfoSerializer(users, many=True)
            return Response({"list_users" : serializer.data})
        except Exception as e:
            logger.error(f"Error searching users: {e}")

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})