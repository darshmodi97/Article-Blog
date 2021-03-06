from django.urls import path
from article_app import views

urlpatterns=[
    path('',views.index,name='index'),
    path('register',views.register,name='register'),
    path('registeruser',views.registeruser,name='registeruser'),
    path('user_dashboard',views.user_dashboard,name='user_dashboard'),
    path('logout_act',views.logout_act,name='logout_act'),
    path('login',views.login,name='login'),
    path('getlogin',views.getlogin,name='getlogin'),
    path('forget_password',views.forget_password,name='forget_password'),
    path('change_password',views.change_password,name='change_password'),
    path('validate_otp',views.validate_otp,name='validate_otp'),
    path('checkusername',views.checkusername,name='checkusername'),
    path('create_article',views.create_article,name='create_article'),
    path('update_profile',views.update_profile,name = 'update_profile'),
    path('show_post',views.show_post,name = 'show_post'),
    path('categorical_post',views.categorical_post,name='categorical_post'),
    path('search_post',views.search_post,name='search_post'),
]