USE_TOTAL_SHAKE_TURN = -1


class ViettelShake:
    BASE_URL = 'https://vtpay8.viettel.vn/shake-2020'
    REQUEST_LOGIN_URL = '{}/user/request-login'.format(BASE_URL)
    LOGIN_URL = '{}/user/login'.format(BASE_URL)
    PROFILE_URL = '{}/user/profile'.format(BASE_URL)
    SHAKE_URL = '{}/game/play'.format(BASE_URL)


class Status:
    SUCCESS = '00'
