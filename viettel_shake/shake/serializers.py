from rest_framework import serializers

from .consts import USE_TOTAL_SHAKE_TURN
from .models import Shake


def get_default_shake_turn():
    return USE_TOTAL_SHAKE_TURN


class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    otp = serializers.CharField()
    shake_turn = serializers.IntegerField(
        default=get_default_shake_turn,
        min_value=-1,
        required=False
    )  # if shake_turn set to -1, then use total turn left


class RequestLoginSerializer(serializers.Serializer):
    user_id = serializers.CharField()


class ShakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shake
        fields = '__all__'
