import io
from django.http import HttpResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from api.models import Post, User
from api.serializers import post_serializer, user_serializer


class post(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        # TODO algorithm this thing
        posts = Post.objects.all()
        serializer = post_serializer(posts, many=True)

        return Response(serializer.data[::-1])

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        data = JSONParser().parse(stream_data)

        pid = request.GET.get("id", 0)
        if pid == 0:
            serializer_data = post_serializer(data=data)

            if serializer_data.is_valid():
                serializer_data.save(created_by=user, image_contents=None)

                response = "True"
            else:
                print(serializer_data.errors)
        else:

            post = Post.objects.get(id=pid, created_by=user)
            serializer_data = post_serializer(post, data=data, partial=True)

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

        serializer_data = post_serializer(data=data)

        if serializer_data.is_valid():
            serializer_data.save(created_by=user, image_contents=file_obj)
            response = "True"
        else:
            print(serializer_data.errors)

        return HttpResponse(response)


class user(APIView):
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

        serializer = user_serializer(user_data, many=False, context=context)

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        response = "False"

        # TODO edit user

        return HttpResponse(response)

    def put(self, request):
        user = request.user
        # TODO create user

        return HttpResponse("False")
