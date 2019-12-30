import json
import logging
from random import randint

from celery import chain
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .consts import USE_TOTAL_SHAKE_TURN
from .cores import ViettelSession
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

    @action(detail=False, methods=['post', ])
    def request_login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        session = ViettelSession(user_id=data['user_id'])
        return Response(session.request_login())

    @action(detail=False, methods=['post', ])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user_id = data['user_id']
        otp = data['otp']
        shake_turn = data['shake_turn']
        session = ViettelSession(user_id=user_id)
        login = session.login(otp=otp)
        logger.info(login)
        profile = session.profile()
        logger.info(profile)
        total_turn_left = profile['data']['totalTurnLeft']
        logger.info('{} total turn left: {}'.format(session.user_id, total_turn_left))
        if shake_turn == USE_TOTAL_SHAKE_TURN:
            shake_turn = total_turn_left
        if shake_turn > 0:
            # dumps headers to string for serializable when send Celery task
            headers_json = json.dumps(dict(session.headers))
            chain(
                shake_task.signature(
                    (headers_json,),
                    immutable=True,  # http://docs.celeryproject.org/en/latest/userguide/canvas.html#immutability
                    countdown=randint(settings.MIN_COUNTDOWN, settings.MAX_COUNTDOWN))
                for _ in range(shake_turn)
            )()
        return Response(session.profile())
