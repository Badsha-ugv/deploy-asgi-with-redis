from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

class UserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.exclude(id=request.user.id)  # Exclude current user
        user_list = [{"id": user.id, "username": user.username} for user in users]
        return Response(user_list)
    


@login_required
def chat_view(request):
    # Get all users except the logged-in user
    users = User.objects.exclude(id=request.user.id).prefetch_related('sent_messages', 'received_messages')
    
    # Prepare user list with last message
    user_list = []
    for user in users:
        # Get the last message between the current user and this user
        last_message = Message.objects.filter(
            Q(sender=request.user, receiver=user) | 
            Q(sender=user, receiver=request.user)
        ).order_by('-timestamp').first()
        
        user_list.append({
            'id': user.id,
            'username': user.username,
            'last_message': last_message.content if last_message else None,
            'last_message_time': last_message.timestamp if last_message else None
        })
    
    return render(request, 'chat.html', {'users': user_list})


class MessageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        # Get messages between the logged-in user and the specified user
        messages = Message.objects.filter(
            Q(sender=request.user, receiver_id=user_id) | 
            Q(sender_id=user_id, receiver=request.user)
        ).order_by('timestamp')
        
        message_list = [{
            'sender': msg.sender.username,
            'content': msg.content,
            'timestamp': msg.timestamp.isoformat()
        } for msg in messages]
        
        return Response(message_list)