from django.urls import path, include
from . import views
from users.views import Register,create_balance

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('register/', Register.as_view(), name='register'),
path('profile', views.profile, name='profile'),

path('balance/', views.create_balance, name='balance'),
    path('create_balance/', views.create_balance, name='create_balance'),
    path('report/<int:balance_id>/', views.report, name='report'),
    path('profile/', views.profile, name='profile'),
    path('balance/edit/<int:balance_id>/', views.edit_balance, name='edit_balance'),
]
