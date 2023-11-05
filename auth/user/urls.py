from django.urls import path, include
from . import views


urlpatterns = [  
    path('register/', views.registerView.as_view(), name='register'),
    path('login/', views.loginView.as_view(), name='login'),
    path('user/', views.userView.as_view()),
    path('logout/', views.logoutView.as_view(), name='logout'),

    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('visits/', views.visit, name='visits'),
    path('reviews/', views.reviews, name='reviews'),

    #user part

    #Children's Homes user functionality
    path('children_orphanages/', views.children_orphanages, name='children_orphanages'),
    path('orphanage/search/', views.orphanage_search, name='search_children_orphanage'),
    path('orphanage/<int:id>/', views.orphanage_detail, name='orphanage_detail'),
    path('orphanage/<int:id>/submit_review/', views.submit_review, name='submit_review'),
    path('orphanage/<int:id>/schedule_visit/', views.schedule_visit, name='schedule_visit'),
    #Donations
    path('donations/', views.donations, name='donations'),
    path('orphanage/<int:id>/donate/', views.make_donations, name='make_donations'),

    #chief part
    path('chief_dashboard/', views.chief_dashboard, name='chief_dashboard'),
    #crud on users
    path('users/', views.all_users, name='users'),
    path('add_user/', views.add_user, name='add_user'),
    #CRUD on homes
    path('add_orphanage', views.add_orphanage, name='add_orphanage'),
    path('edit_home/<int:id>/', views.edit_orphanage, name='edit_orphanage'),
    path('delete_home/<int:id>/', views.delete_orphanage, name='delete_orphanage'),
    path('analytics/most_visited_home', views.most_visited_home, name='most_visited_home'),
    path('analytics/most_in_need_home', views.most_in_need_home, name='most_in_need_home'),
    
]