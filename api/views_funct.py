from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.models import User, Follow
from api.serializers import UserSerializer


@api_view(['GET'])
@action(detail=True, permission_classes=[IsAuthenticated])
def get_suggested_users(request):
    user = request.user

    # TODO yet another algo here. Make better
    follows = Follow.objects.all().filter(created_by=user)

    usernames = [x.following.username for x in follows]
    usernames.append(user.username)

    all_users = User.objects.all().exclude(username__in=usernames)

    context = {
        'exclude_fields': [
            'email',
            'id',
            'last_login'
        ]
    }

    serializer = UserSerializer(all_users, many=True, context=context)

    return Response(serializer.data)
