import io
from django.http import HttpResponse
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from api.models import Post
from api.serializers import post_serializer


class post(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)

    def get(self, request):
        # TODO algorithm this thing
        posts = Post.objects.all().reverse()
        serializer = post_serializer(posts, many=True)

        return Response(serializer.data)

    def post(self, request):
        user = request.user
        response = "False"

        JSON_datatype = request.body
        stream_data = io.BytesIO(JSON_datatype)
        data = JSONParser().parse(stream_data)

        file_obj = len(request.POST)
        print(file_obj)

        pid = request.GET.get("id", 0)
        image = data["image_contents"]
        print(image)

        if pid == 0:
            serializer_data = post_serializer(data=data)

            if serializer_data.is_valid():
                image = None



                serializer_data.save(created_by=user, image_contents=image)

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
