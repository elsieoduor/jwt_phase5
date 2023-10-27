from django.urls import path, include
from . import views
urlpatterns = [  
    path('register/', views.registerview.as_view()),
    path('login/', views.loginview.as_view()),
    path('user/', views.userview.as_view()),
    path('logout/', views.logoutview.as_view()),
]