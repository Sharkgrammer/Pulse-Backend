import string
from datetime import timedelta

from django.utils import timezone
from dateutil import parser
import random
import time
import os
from django.core.exceptions import ValidationError


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


def get_days_ago(days):
    today = get_today()

    return today - timedelta(days=days)


def get_mins_ago(mins):
    today = get_today()

    return today - timedelta(minutes=mins)


def generate_random_string(n=10):
    return ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=n))


def validate_image(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.apng', 'avif']

    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported image extension')


def update_follows(user, following, add):
    if add:
        user.following += 1
        following.followers += 1
    else:
        user.following -= 1
        following.followers -= 1

    user.save()
    following.save()


def update_likes(model, add):
    if add:
        model.likes += 1
    else:
        model.likes -= 1

    model.save()


def wait_random_amount():
    randTime = random.uniform(0.2, 1)
    print("Waiting {} seconds...".format(randTime))

    time.sleep(randTime)

