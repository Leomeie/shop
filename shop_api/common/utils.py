import os
import uuid
from django.utils import timezone


def generate_order_no():
    now = timezone.now()
    return now.strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[:6].upper()


def generate_payment_no():
    return "PAY" + timezone.now().strftime("%Y%m%d%H%M%S") + uuid.uuid4().hex[:8].upper()


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()
