from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('<str:username>/', views.user_detail, name='user-detail'),
    path('user/edit/', views.edit_profile, name='edit-profile'),
    path('user/leave/', views.leave, name='leave'),
    path('certificate/', views.request_certificate, name='request-certificate'),
]
