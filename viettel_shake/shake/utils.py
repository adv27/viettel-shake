from .models import ViettelUser


def ensure_viettel_user(phone):
    """
    Check if Viettel user exits, else create the new one
    :param phone: Viettel phone number
    :return: ViettelUser object
    """
    try:
        user = ViettelUser.objects.get(phone=phone)
    except ViettelUser.DoesNotExist:
        user = ViettelUser.objects.create(phone=phone)
        user.save()
    return user
