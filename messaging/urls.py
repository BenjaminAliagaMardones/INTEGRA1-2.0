from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/<int:chat_id>/messages/', views.chat_messages, name='chat_messages'),
    path('direct/<int:user_id>/', views.create_direct_chat, name='create_direct_chat'),
    path('company/<int:company_id>/', views.create_company_chat, name='create_company_chat'),
    path('cooperative/<int:cooperative_id>/', views.create_cooperative_chat, name='create_cooperative_chat'),
]
