from django.utils import timezone
from dateutil import parser
import random


def convert_web_date_to_datetime(date_str):
    if date_str != "":
        return parser.parse(date_str)
    else:
        return ""


def convert_datetime_to_web_date(time, time_format="%A, %H:%M:%S, %d %b %Y"):
    result_time = time.strftime(time_format)
    return result_time


def get_today():
    return timezone.now()


def generate_random_string(n):
    random_string = ""

    for _ in range(n):
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)

        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        random_string += (chr(random_integer))

    return random_string


def update_follows(user, following, add):
    if add:
        user.following += 1
        following.followers += 1
    else:
        user.following -= 1
        following.followers -= 1

    user.save()
    following.save()


def update_likes(post, add):
    if add:
        post.likes += 1
    else:
        post.likes -= 1

    post.save()
