from django.urls import path
from article_app import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('registeruser',views.registeruser,name='registeruser'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('logout',views.logout,name='logout'),
    path('login',views.login,name='login'),
    path('getlogin',views.getlogin,name='getlogin'),
    path('create_article',views.create_article,name='create_article'),



]