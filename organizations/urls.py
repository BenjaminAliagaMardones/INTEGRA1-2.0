from django.urls import path
from . import views

app_name = 'organizations'

urlpatterns = [
    # Company URLs
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.company_create, name='company_create'),
    path('companies/<int:pk>/', views.company_detail, name='company_detail'),
    path('companies/<int:pk>/join/', views.company_join, name='company_join'),
    path('companies/<int:pk>/leave/', views.company_leave, name='company_leave'),
    path('companies/<int:pk>/edit/', views.company_edit, name='company_edit'),
    path('companies/<int:pk>/delete/', views.company_delete, name='company_delete'),
    
    # Cooperative URLs
    path('cooperatives/', views.cooperative_list, name='cooperative_list'),
    path('cooperatives/create/', views.cooperative_create, name='cooperative_create'),
    path('cooperatives/<int:pk>/', views.cooperative_detail, name='cooperative_detail'),
    path('cooperatives/<int:pk>/join/', views.cooperative_join, name='cooperative_join'),
    path('cooperatives/<int:pk>/leave/', views.cooperative_leave, name='cooperative_leave'),
    path('cooperatives/<int:pk>/edit/', views.cooperative_edit, name='cooperative_edit'),
    path('cooperatives/<int:pk>/delete/', views.cooperative_delete, name='cooperative_delete'),
]
