from api.functions.functions import generate_random_string
from api.models import Post


def generate_pid():
    pid = generate_random_string(10)
    pid_exists = Post.objects.filter(pid=pid).exists()

    if pid_exists:
        pid = generate_pid()

    return pid
