from django.urls import path
from . import views
from .views import signup   # 👈 ADD THIS LINE

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', signup, name='signup'),
]