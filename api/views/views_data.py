import io

from django.http import HttpResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.functions.functions import update_follows, update_likes, get_today, wait_random_amount
from api.functions.functions_model import generate_pid
from api.models import Post, User, Follow, Like, Comment, Interest, Interest_User
from api.serializers import PostSerializer, UserSerializer, FollowSerializer, LikeSerializer, CommentSerializer, \
    InterestSerializer


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        pid = request.GET.get("pid", None)
        user = request.user
        context = {
            'user': user
        }

        if pid is None:
            # Get all posts
            # TODO algorithm this thing

            amt = int(request.GET.get('amt', 7))

            # TODO remove this, it just makes the UX feel more hefty when ran locally
            if amt > 7:
                wait_random_amount()

            posts = Post.objects.all().order_by('-id')[:amt:1]
            serializer = PostSerializer(posts, many=True, context=context)

        else:
            post = Post.objects.get(pid=pid)
            serializer = PostSerializer(post, many=False, context=context)

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        data = JSONParser().parse(stream_data)

        pid = request.GET.get("pid", None)

        # TODO remove this, it just makes the UX feel more hefty when ran locally
        wait_random_amount()

        if pid is None:
            serializer_data = PostSerializer(data=data)

            if serializer_data.is_valid():
                post_pid = generate_pid()
                serializer_data.save(created_by=user, image_contents=None, pid=post_pid)

                response = "True"
            else:
                print(serializer_data.errors)
        else:

            post = Post.objects.get(id=pid, created_by=user)
            serializer_data = PostSerializer(post, data=data, partial=True)

            if serializer_data.is_valid():
                serializer_data.save(org=user.org)
                response = "True"
            else:
                print(serializer_data.errors)

        return HttpResponse(response)

    def put(self, request):
        user = request.user
        file_obj = request.FILES['file']
        response = "False"

        # TODO remove this, it just makes the UX feel more hefty when ran locally
        wait_random_amount()

        data = {'image_post': True, 'content': request.data['content']}

        serializer_data = PostSerializer(data=data)

        if serializer_data.is_valid():
            post_pid = generate_pid()
            serializer_data.save(created_by=user, image_contents=file_obj, pid=post_pid)
            response = "True"
        else:
            print(serializer_data.errors)

        return HttpResponse(response)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user

        logging_in = request.GET.get("lin", False)

        if logging_in:
            user.last_login = get_today()
            user.save()

        uid = request.GET.get("username", None)
        email = request.GET.get("email", None)

        if uid is None and email is None:
            return HttpResponse("False")

        # TODO if i implement block/privacy features, they would go here and in the post algo
        user_data = None

        if email is None:
            user_data = User.objects.get(username=uid)
        else:
            user_data = User.objects.get(email=email)

        context = {}
        if user.username != uid:
            context = {
                'exclude_fields': [
                    'email',
                    'id',
                    'last_login'
                ]
            }

        serializer = UserSerializer(user_data, many=False, context=context)

        return Response(serializer.data)


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        # Get all follows or followers for a user
        user = request.user

        username = user.username
        get_followers = request.GET.get("followers", None) == "true"

        if get_followers is not None:
            data = Follow.objects.all()

            # The follow data itself is rather useless for the front end. Get a list of users now
            if get_followers:
                data = data.filter(following__username=username, deleted=False).values("created_by__username")
            else:
                data = data.filter(created_by__username=username, deleted=False).values("following__username")

            all_users = User.objects.filter(username__in=data).exclude(username=user.username)

            context = {
                'exclude_fields': [
                    'email',
                    'id',
                    'last_login'
                ],
                'user': user
            }

            serializer = UserSerializer(all_users, many=True, context=context)

            return Response(serializer.data)
        else:
            return HttpResponse("False")

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        JSON_data = JSONParser().parse(stream_data)

        username = JSON_data["username"]

        if username is not None:
            follow_user = User.objects.get(username=username)
            test_follow = Follow.objects.filter(created_by=user, following=follow_user)
            add_follow = False

            if test_follow.exists():
                follow = test_follow[0]

                add_follow = follow.deleted
                follow.deleted = not follow.deleted
                follow.last_update = get_today()

                follow.save()
                response = "True"
            else:
                serializer_data = FollowSerializer(data={})

                if serializer_data.is_valid():
                    serializer_data.save(created_by=user, following=follow_user)
                    add_follow = True

                    response = "True"

            update_follows(user, follow_user, add_follow)

        return HttpResponse(response)


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return HttpResponse("False")

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        JSON_data = JSONParser().parse(stream_data)

        if "pid" in JSON_data:
            pid = JSON_data["pid"]
            post = Post.objects.get(pid=pid)
            test_like = Like.objects.filter(created_by=user, post=post)
            add_like = False

            if test_like.exists():
                like = test_like[0]

                add_like = like.deleted
                like.deleted = not like.deleted
                like.last_update = get_today()

                like.save()
                response = "True"
            else:
                serializer_data = LikeSerializer(data={})

                if serializer_data.is_valid():
                    serializer_data.save(created_by=user, post=post)
                    add_like = True

                    response = "True"

            update_likes(post, add_like)


        elif "cid" in JSON_data:
            cid = JSON_data["cid"]
            comment = Comment.objects.get(id=cid)
            test_like = Like.objects.filter(created_by=user, comment=comment)
            add_like = False

            if test_like.exists():
                like = test_like[0]

                add_like = like.deleted
                like.deleted = not like.deleted
                like.last_update = get_today()

                like.save()
                response = "True"
            else:
                serializer_data = LikeSerializer(data={})

                if serializer_data.is_valid():
                    serializer_data.save(created_by=user, comment=comment)
                    add_like = True

                    response = "True"

            update_likes(comment, add_like)

        return HttpResponse(response)


class CommentView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        pid = request.GET.get("pid", None)
        user = request.user
        context = {
            'user': user
        }

        if pid is not None:
            amt = int(request.GET.get('amt', 7))

            # TODO remove this, it just makes the UX feel more hefty when ran locally
            if amt > 7:
                wait_random_amount()

            comments = Comment.objects.filter(post__pid=pid).order_by('-id')[:amt:1]
            serializer = CommentSerializer(comments, many=True, context=context)

            return Response(serializer.data)

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        data = JSONParser().parse(stream_data)

        pid = request.GET.get("pid", None)

        # TODO remove this, it just makes the UX feel more hefty when ran locally
        wait_random_amount()

        if pid is not None:
            serializer_data = CommentSerializer(data=data)
            post = Post.objects.get(pid=pid)

            if serializer_data.is_valid():
                serializer_data.save(created_by=user, post=post)

                # Update post comments. No point in making it a one time function i guess
                post.comments += 1
                post.save()

                response = "True"
            else:
                print(serializer_data.errors)

        return HttpResponse(response)


class InterestView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user
        context = {
            'user': user
        }

        only_interested = request.GET.get("interested", False)
        interests = {}

        if only_interested:
            user_interests = Interest_User.objects.values("interest_id").filter(user=user).exclude(deleted=True)

            interests = Interest.objects.filter(id__in=user_interests)
        else:
            interests = Interest.objects.all().exclude(deleted=True)

        serializer = InterestSerializer(interests, many=True, context=context)

        return Response(serializer.data)
