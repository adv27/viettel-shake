import json

from django.utils import timezone

from config import celery_app
from .cores import ViettelSession
from .models import Shake, ViettelUser


@celery_app.task()
def shake_task(headers_json: str):
    session = ViettelSession()
    session.headers = json.loads(headers_json)
    shake = session.shake()
    # saving response through task
    save_response.delay(
        session.get_user_id(),
        shake,
        timezone.now()  # send current time because task may have been waited
    )
    return shake


@celery_app.task()
def save_response(user_id, json_response, created_at):
    try:
        user = ViettelUser.objects.get(phone=user_id)
    except ViettelUser.DoesNotExist:
        user = ViettelUser.objects.create(phone=user_id)
        user.save()
    new_shake = Shake.objects.create(
        user=user,
        data=json_response,
        created_at=created_at
    )
    new_shake.save()
    return new_shake.id
