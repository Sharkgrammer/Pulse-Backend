from django.urls import path
from api import views

app_name = "api"
urlpatterns = [
    path('post', views.post.as_view(), name='post'),
]
