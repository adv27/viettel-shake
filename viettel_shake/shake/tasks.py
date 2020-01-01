import json

from config import celery_app
from .cores import ViettelSession
from .models import Shake
from .utils import ensure_viettel_user


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
    # saving response
    viettel_user = ensure_viettel_user(phone)
    new_shake = Shake.objects.create(
        user=viettel_user,
        data=shake
    )
    new_shake.save()
    return shake
