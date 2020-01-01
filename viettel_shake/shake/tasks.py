import json

from django.utils import timezone

from config import celery_app
from .cores import ViettelSession
from .models import Shake, ViettelUser


@celery_app.task()
def shake_task(phone: str, headers_json: str):
    """
    Make shake request through celery task
    :param phone: Viettel phone number
    :param headers_json: authenticated headers
    :return: JSON response of shake request
    """
    session = ViettelSession(phone)
    session.headers = json.loads(headers_json)  # re-binding headers with authenticated headers
    shake = session.shake()
    # saving response through task
    save_response.delay(
        session.phone,
        shake,
        timezone.now()  # send current time because task may have been waited
    )
    return shake


@celery_app.task()
def save_response(phone, json_response, created_at):
    try:
        user = ViettelUser.objects.get(phone=phone)
    except ViettelUser.DoesNotExist:
        user = ViettelUser.objects.create(phone=phone)
        user.save()
    new_shake = Shake.objects.create(
        user=user,
        data=json_response,
        created_at=created_at
    )
    new_shake.save()
    return new_shake.id
