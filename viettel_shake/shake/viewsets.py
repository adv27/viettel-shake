import json
import logging
from http import HTTPStatus
from random import randint

from celery import chain
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from requests import HTTPError
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .consts import USE_TOTAL_SHAKE_TURN
from .cores import ViettelSession
from .exceptions import LoginFailed
from .models import ViettelUser
from .serializers import LoginSerializer, RequestLoginSerializer
from .tasks import shake_task

logger = logging.getLogger(__name__)


class ViettelShakeViewSet(viewsets.GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'request_login':
            return RequestLoginSerializer

        if self.action == 'login':
            return LoginSerializer

        return super().get_serializer_class()

    @swagger_auto_schema(
        operation_description="Request Viettel to send OTP to user's phone number"
    )
    @action(detail=False, methods=['post', ])
    def request_login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        session = ViettelSession(phone=data['phone'])
        return Response(session.request_login())

    @swagger_auto_schema(
        operation_description='Make login request with OTP\n'
                              'If shake_turn is not -1, then use total shake turn left of user'
    )
    @action(detail=False, methods=['post', ])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        phone = data['phone']
        otp = data['otp']
        shake_turn = data['shake_turn']
        is_admin = request.user and request.user.is_staff  # only admin can override shake turn
        session = ViettelSession(phone=phone)
        try:
            login = session.login(otp=otp)
            logger.info(login)
        except (HTTPError, LoginFailed):
            return Response({'error': 'Login failed!'}, status=HTTPStatus.UNAUTHORIZED)
        # create Viettel user instance when login success
        new_viettel_user = ViettelUser.objects.create(phone=phone)
        new_viettel_user.save()
        # request profile of Viettel user
        profile = session.profile()
        logger.info(profile)
        total_turn_left = profile['data']['totalTurnLeft']
        logger.info('{} total turn left: {}'.format(session.user_id, total_turn_left))
        if not is_admin or shake_turn == USE_TOTAL_SHAKE_TURN:
            shake_turn = total_turn_left
        if shake_turn > 0:
            # dumps headers to string for serializable when send Celery task
            headers_json = json.dumps(dict(session.headers))
            chain(
                shake_task.signature(
                    (phone, headers_json),
                    immutable=True,  # http://docs.celeryproject.org/en/latest/userguide/canvas.html#immutability
                    countdown=randint(settings.MIN_COUNTDOWN, settings.MAX_COUNTDOWN))
                for _ in range(shake_turn)
            )()
        return Response(session.profile())
