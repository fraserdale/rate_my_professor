from django.urls import path
from rango import views

app_name = 'rango'

urlpatterns = [
    path('index', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('recent/', views.recent, name='recent'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('professors/', views.professors, name='professors'),
    path('professor/<slug:professor_name_slug>', views.show_professor, name='show_professor'),
    #path('professor/<slug:professor_name_slug>/review', views.professor_review, name='professor_review')

]
