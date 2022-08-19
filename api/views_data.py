import io
from django.http import HttpResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.functions import update_follows
from api.models import Post, User, Follow
from api.serializers import PostSerializer, UserSerializer, FollowSerializer


class PostView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        # TODO algorithm this thing
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data[::-1])

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        data = JSONParser().parse(stream_data)

        pid = request.GET.get("id", 0)
        if pid == 0:
            serializer_data = PostSerializer(data=data)

            if serializer_data.is_valid():
                serializer_data.save(created_by=user, image_contents=None)

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

        data = {'image_post': True, 'content': request.data['content']}

        serializer_data = PostSerializer(data=data)

        if serializer_data.is_valid():
            serializer_data.save(created_by=user, image_contents=file_obj)
            response = "True"
        else:
            print(serializer_data.errors)

        return HttpResponse(response)


class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        user = request.user

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

    def post(self, request):
        user = request.user
        response = "False"

        # TODO edit user

        return HttpResponse(response)

    def put(self, request):
        user = request.user
        # TODO create user (with image)

        return HttpResponse("False")


class FollowView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        # Get all follows or followers a user

        username = request.GET.get("u", None)
        is_followers = request.GET.get("f", None)

        if username is not None and is_followers is not None:
            follow_data = {}

            if is_followers:
                follow_data = Follow.objects.all().filter(created_by__username=username)
            else:
                follow_data = Follow.objects.all().filter(following__username=username)

            serializer = FollowSerializer(follow_data, many=True)

            return Response(serializer.data)
        else:
            return HttpResponse("False")

    def post(self, request):
        print(request)
        user = request.user
        response = "False"
        print(request)

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        JSON_data = JSONParser().parse(stream_data)

        username = JSON_data["username"]

        if username is not None:
            follow_user = User.objects.get(username=username)
            test_follow = Follow.objects.filter(created_by=user, following=follow_user)

            if test_follow.exists():
                test_follow.delete()
                update_follows(user, follow_user, False)
                response = "True"

            else:
                serializer_data = FollowSerializer(data={})

                if serializer_data.is_valid():
                    serializer_data.save(created_by=user, following=follow_user)
                    update_follows(user, follow_user, True)

                    response = "True"

        return HttpResponse(response)


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return HttpResponse("False")

    def post(self, request):
        return HttpResponse("False")
