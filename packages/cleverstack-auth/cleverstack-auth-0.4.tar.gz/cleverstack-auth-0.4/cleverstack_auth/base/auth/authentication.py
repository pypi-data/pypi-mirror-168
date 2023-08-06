from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from threading import local

_thread_locals = local()


def set_current_instance_field(name, value):
    setattr(_thread_locals, name, value)


class JSONWebTokenAuthentication(JWTAuthentication):

    def authenticate(self, request):
        authorization = request.META.get("HTTP_AUTHORIZATION", None)
        self.org = request.META.get("HTTP_COMPANY", None)
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        set_current_instance_field("authorization", True)
        return self.get_user(validated_token), validated_token


class TokenAuthMiddleware(object):
    """adding profile and company to request object
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        try:
            token_auth_user = JSONWebTokenAuthentication().authenticate(request)
        except exceptions.AuthenticationFailed:
            token_auth_user = None
        if isinstance(token_auth_user, tuple):
            request.user = token_auth_user[0]


class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Bearer'

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired, token = token_expire_handler(token)

        return token.user, token


def is_token_expired(token):
    user_last_login = Token.objects.get(key=token).user.last_login
    if user_last_login:
        today = timezone.now()
        if (today - user_last_login).days >= 7:
            return True
        else:
            return False
    else:
        return False


def token_expire_handler(token):
    is_expired = is_token_expired(token)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)
    return is_expired, token
