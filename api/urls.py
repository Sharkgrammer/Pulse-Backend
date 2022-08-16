from django.urls import path
from api import views_data as data
from api import views_funct as funct

app_name = "api"
urlpatterns = [
    # Data based views
    path('post', data.PostView.as_view(), name='post'),
    path('user', data.UserView.as_view(), name='user'),
    path('follow', data.FollowView.as_view(), name='follow'),
    path('like', data.LikeView.as_view(), name='like'),

    # Function based views
    path('get_suggested_users', funct.get_suggested_users, name='get_suggested_users'),

]
