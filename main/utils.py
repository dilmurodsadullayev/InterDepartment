import random
import string

from django.shortcuts import get_object_or_404

from config import settings
from main.models import ApplicationUser

def generate_numeric_mega_id(length=8):
    mega_id = ''.join(random.choices('0123456789', k=length))
    return mega_id


def generate_password(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


