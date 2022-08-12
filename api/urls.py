from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path('post', views.post.as_view(), name='post'),
    path('user', views.user.as_view(), name='user'),
    path('get_suggested_users', views.get_suggested_users, name='get_suggested_users'),
]
