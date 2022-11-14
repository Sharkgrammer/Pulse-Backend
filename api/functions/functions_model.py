from api.functions.functions import generate_random_string, get_days_ago
from api.models import Follow, Post, Interest_User, Comment, Like


def generate_pid():
    pid = generate_random_string(10)
    pid_exists = Post.objects.filter(pid=pid).exists()

    if pid_exists:
        pid = generate_pid()

    return pid


def get_user_score(main_user, other_user):
    # Get how many followers are in common
    other_follows = Follow.objects.values("following__username").filter(created_by=other_user, deleted=False)

    similar_follows = Follow.objects.filter(following__username__in=other_follows, created_by=main_user,
                                            deleted=False).count()

    # Get how many interests are in common
    other_interests = Interest_User.objects.values("interest__name").filter(user=other_user, deleted=False)

    similar_interests = Interest_User.objects.filter(interest__name__in=other_interests, user=main_user,
                                                     deleted=False).count()

    # Check if the user has posted recently.
    posted = Post.objects.filter(created_by=other_user, deleted=False, created_date__gte=get_days_ago(3)).exists()

    score = similar_follows + similar_interests
    if posted:
        score *= 2

        if score == 0:
            score += 1

    # Check if the user logged in in the past day
    if other_user.last_login >= get_days_ago(1):
        score += 1

    # Check if main has interacted with the user via likes or comments
    score += Comment.objects.filter(created_by=main_user, post__created_by=other_user,
                                    created_date__gte=get_days_ago(3), deleted=False).count()
    score += Like.objects.filter(created_by=main_user, post__created_by=other_user, created_date__gte=get_days_ago(3),
                                 deleted=False).count()

    # These two scores are based on current twitter drama thanks to musk.
    # Check if the user is verified
    if other_user.verified:
        score += 1

    # Check if the user is the big cheese
    # if other_user.username == "@admin":
        # score += 1

    return score
