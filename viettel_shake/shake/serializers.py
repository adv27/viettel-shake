from rest_framework import serializers

from .consts import USE_TOTAL_SHAKE_TURN
from .models import Shake, ViettelUser


def get_default_shake_turn():
    return USE_TOTAL_SHAKE_TURN


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    otp = serializers.CharField()
    shake_turn = serializers.IntegerField(
        default=get_default_shake_turn,
        min_value=-1,
        required=False
    )  # if shake_turn set to -1, then use total turn left


class RequestLoginSerializer(serializers.Serializer):
    phone = serializers.CharField()


class ShakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shake
        fields = '__all__'


class ViettelUserSerializer(serializers.ModelSerializer):
    shakes = ShakeSerializer(many=True, read_only=True)

    class Meta:
        model = ViettelUser
        fields = ('phone', 'shakes',)
