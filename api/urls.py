from django.urls import path
from api.views import views_data as data, views_funct as funct

app_name = "api"
urlpatterns = [

    # Data based views
    path('post', data.PostView.as_view(), name='post'),
    path('user', data.UserView.as_view(), name='user'),
    path('follow', data.FollowView.as_view(), name='follow'),
    path('like', data.LikeView.as_view(), name='like'),
    path('comment', data.CommentView.as_view(), name='comment'),
    path('interest', data.InterestView.as_view(), name='interest'),

    # Function based views
    path('get_suggested_users', funct.get_suggested_users, name='get_suggested_users'),
    path('update_post_shares', funct.update_post_shares, name='update_post_shares'),
    path('update_interests', funct.update_interests, name='update_interests'),
    path('username_free', funct.username_free, name='username_free'),
    path('email_free', funct.email_free, name='email_free'),
    path('create_user', funct.create_user, name='create_user'),
    path('get_all_interests', funct.get_all_interests, name='get_all_interests'),

]
