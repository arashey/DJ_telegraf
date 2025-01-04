from django.urls import path
from . views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', register, name='register'),
    path('verify/', verify, name='verify'),
    path('login/', login_view, name='login'),
    path('', chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', chat_detail, name='chat_detail'),
    path('chat/create/', create_chat, name='create_chat'),
    path('chats/create_group/', create_group, name='create_group'),
    path('edit_message/<int:message_id>/', edit_message, name='edit_message'),
    path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
    path('add_participant/<int:chat_id>/', add_participant, name='add_participant'),
    path('mark_notifications_as_read/', mark_notifications_as_read, name='mark_notifications_as_read'),
    path("find_user/", find_user_and_create_chat, name="find_user_and_create_chat"),
    path("profile/", create_or_edit_profile, name="create_edit_profile"),
    path('profile/<int:user_id>/', profile_detail, name='profile_detail'),
    path('delete_chat/<int:chat_id>/', delete_chat, name='delete_chat'),
    path('profile/delete-avatar/', delete_avatar, name='delete_avatar'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
