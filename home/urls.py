from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('profile', views.profile, name='profile'),
    path('academic', views.academic, name='academic'),
    path('log_out', views.log_out, name='log_out'),
    path('attendence', views.attendence, name='attendence')
]