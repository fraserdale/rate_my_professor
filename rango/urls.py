from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('index', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),

]
