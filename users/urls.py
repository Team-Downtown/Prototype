from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/',views.SignUp.as_view(), name = 'signup'),
    path('view/',views.view_user_info, name='view-user'),
    path('update/',views.update_user, name = 'update-user'),
    path('change-password/', views.change_password_view, name='change-password'),
    path('users/',views.UserListView.as_view(), name='user-list'),

]
