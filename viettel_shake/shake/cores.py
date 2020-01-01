import logging

from requests import Session
from requests.exceptions import RequestException
from requests.utils import default_headers

from .consts import Status, ViettelShake
from .exceptions import LoginFailed


class ViettelSession(Session):
    def __init__(self, phone):
        """
        :param phone: Viettel phone number
        """
        super().__init__()
        self.phone = phone
        self.user_id = self.phone_number_2_user_id()
        headers = default_headers()
        headers.update({
            'Password': 'digital@2020',
            'Channel': 'APP',
            'User-Agent': 'ViettelPay/3.3.1 (iPhone; iOS 13.3; Scale/3.00)',
            'User-Id': self.user_id
        })
        self.headers = headers  # bind headers

    def phone_number_2_user_id(self):
        """
        Striping pre-fix '0' from phone_number
        """
        return self.phone[1:] if self.phone[0] == '0' else self.phone

    def request_login(self):
        """
        Request Viettel server to send OTP to phone number (user_id)
        :return: JSON response
        """
        r_request_login = self.get(ViettelShake.REQUEST_LOGIN_URL)
        r_request_login.raise_for_status()
        json_response = r_request_login.json()
        return json_response

    def login(self, otp: str):
        """
        Make login POST request then grab token in the response if success
        :param otp: OTP code that send to user's phone
        :return: JSON response
        """
        data = {
            'otp': otp
        }
        r_login = self.post(ViettelShake.LOGIN_URL, json=data)
        r_login.raise_for_status()
        json_response = r_login.json()
        if 'status' in json_response and json_response['status']['code'] == Status.SUCCESS:
            '''
            Login success -> bind token to headers
            '''
            token = json_response['data']['token']
            headers = self.headers
            headers.update({
                'Authorization': token
            })
            self.headers = headers
        else:
            logging.error('Login failed!', extra=json_response)  # this event is sent to Sentry
            # raise login failed
            raise LoginFailed('Login failed!')
        return json_response

    def profile(self):
        if 'Authorization' not in self.headers:
            raise RequestException('Not login yet!')
        r_profile = self.get(ViettelShake.PROFILE_URL)
        r_profile.raise_for_status()
        json_response = r_profile.json()
        return json_response

    def shake(self):
        if 'Authorization' not in self.headers:
            raise RequestException('Not login yet!')
        r_shake = self.post(ViettelShake.SHAKE_URL)
        r_shake.raise_for_status()
        json_response = r_shake.json()
        return json_response
