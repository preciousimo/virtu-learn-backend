from django.urls import path
from . import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout, name="logout"),
]