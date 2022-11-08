import io
from itertools import chain

from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import action, api_view
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.functions.functions import wait_random_amount
from api.models import Follow, User, Post, Interest, Interest_User
from api.serializers import UserSerializer, InterestSerializer, PostSerializer, SuggestedUserSerializer


@api_view(['GET'])
@action(detail=True, permission_classes=[IsAuthenticated])
def get_suggested_users(request):
    user = request.user

    # Get all users that you don't follow. Exclude yourself
    usernames = Follow.objects.values("following__username").filter(created_by=user, deleted=False)
    all_users = User.objects.all().exclude(username__in=usernames).exclude(username=user.username)

    # Run the suggested user serializer. Calculates a score based on mutual follows/interests
    serializer = SuggestedUserSerializer(all_users, many=True, context={'user': user})

    # Sort data in reverse based on the score. Highest is best
    sorted_data = sorted(serializer.data, key=lambda u: u['score'], reverse=True)

    # return the 6 best scores
    return Response(sorted_data[:6:1])


@api_view(['GET'])
@action(detail=True, permission_classes=[IsAuthenticated])
def update_post_shares(request):
    pid = request.GET.get("pid", None)

    if pid is not None:
        post = Post.objects.get(pid=pid)

        post.shares += 1
        post.save()

    return HttpResponse("True")


@api_view(['POST'])
@action(detail=True, permission_classes=[IsAuthenticated])
def update_interests(request):
    user = request.user

    JSON_datatype = request.body
    stream_data = io.BytesIO(JSON_datatype)
    data = JSONParser().parse(stream_data)

    interests = data["interests"]
    new_interests = []

    # Create a new interest if it doesn't already exist
    # TODO Probably needs moderation if this was to go into prod
    for interest in interests:
        name = interest["name"]
        new_interests.append(name)

        i_exists = Interest.objects.filter(name=name).exists()

        if not i_exists:
            serializer_data = InterestSerializer(data=interest)

            if serializer_data.is_valid():
                serializer_data.save()
            else:
                print(serializer_data.errors)

    # Check the users interests. The i_names list contains every interest they want/are interested in
    old_interests = Interest_User.objects.values_list("interest__name", flat=True).filter(user=user, deleted=False)
    old_interests = list(old_interests)

    for new in new_interests:
        if new in old_interests:
            # New interest already is marked as existing
            old_interests.remove(new)

    # If theres an old interest here, remove it from existence
    for old in old_interests:
        # Can't do this in the other loop without breaking it
        if old in new_interests:
            new_interests.remove(old)

        old_i = Interest.objects.get(name=old)
        old_i.count -= 1
        old_i.save()

        old_iu = Interest_User.objects.get(interest=old_i, user=user)
        old_iu.deleted = True
        old_iu.save()

    for add in new_interests:
        add_i = Interest.objects.get(name=add)
        add_i.count += 1
        add_i.save()

        interest_exists = Interest_User.objects.filter(user=user, interest=add_i).exists()
        if interest_exists:
            new_i = Interest_User.objects.get(user=user, interest=add_i)
            new_i.deleted = False
            new_i.save()

        else:
            new_i = Interest_User.objects.create(user=user, interest=add_i)
            new_i.save()

    return HttpResponse("True")


@api_view(['GET'])
@action(detail=False)
def username_free(request):
    username = "@" + request.GET.get("username", "")
    response = "False"

    if username != "@":
        response = not User.objects.filter(username=username).exists()

    return HttpResponse(response)


@api_view(['GET'])
@action(detail=False)
def email_free(request):
    email = request.GET.get("email", "")
    response = "False"

    if email != "":
        response = not User.objects.filter(email=email).exists()

    return HttpResponse(response)


@api_view(['PUT'])
@action(detail=True, permission_classes=[MultiPartParser])
def create_user(request):
    file_obj = request.FILES['file']
    response = "False"

    # TODO remove this, it just makes the UX feel more hefty when ran locally
    wait_random_amount()

    password = make_password(request.data["password"])

    data = {'first_name': request.data['first_name'], 'last_name': request.data['last_name'],
            'email': request.data['email'], 'username': '@' + request.data['username'],
            'prof_desc': request.data['prof_desc']}

    serializer_data = UserSerializer(data=data)

    if serializer_data.is_valid():
        serializer_data.save(prof_image=file_obj, password=password)
        response = "True"
    else:
        print(serializer_data.errors)

    return HttpResponse(response)


@api_view(['GET'])
@action(detail=False)
def get_all_interests(request):
    interests = Interest.objects.all().exclude(deleted=True)

    serializer = InterestSerializer(interests, many=True)

    return Response(serializer.data)


@api_view(['GET'])
@action(detail=False)
def search(request):
    # Search through users and posts
    user = request.user
    context = {
        'user': user,
        'exclude_fields': [
            'email',
            'id',
            'last_login'
        ]
    }

    query = request.GET.get("query", "")
    user_amt = int(request.GET.get('uamt', 3))
    post_amt = int(request.GET.get('pamt', 3))

    users = User.objects.all().filter(
        Q(first_name__contains=query) | Q(last_name__contains=query) | Q(username__contains=query),
        is_active=True).order_by('-id').exclude(username=user.username)[:user_amt:1]

    posts = Post.objects.all().filter(Q(content__contains=query), deleted=False).order_by('-id')[:post_amt:1]

    # TODO i don't know how bad this will be speed wise
    user_serial = SuggestedUserSerializer(users, many=True, context=context)
    user_data = sorted(user_serial.data, key=lambda u: u['score'], reverse=True)

    post_serial = PostSerializer(posts, many=True, context=context)

    data = chain(user_data, post_serial.data)

    return Response(data)
