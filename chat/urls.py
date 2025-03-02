from django.urls import path
from .views import UserListView,chat_view, MessageHistoryView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('messages/<int:user_id>/', MessageHistoryView.as_view(), name='message-history'),
    path('', chat_view, name='chat'),
]