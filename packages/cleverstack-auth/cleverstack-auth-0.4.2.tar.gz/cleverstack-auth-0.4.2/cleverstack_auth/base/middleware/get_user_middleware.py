from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject
from rest_framework.authtoken.models import Token


class GetUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    @staticmethod
    def get_user(request):
        user = get_user(request)
        if user.is_authenticated:
            return user
        try:
            token = Token.objects.get(
                key=request.headers['Authorization'].split()[1])
            user = User.objects.get(pk=token.user_id)
        except Exception as error:
            print(error)
            pass
        return user

    def __call__(self, request):
        request.user = SimpleLazyObject(
            lambda: self.__class__.get_user(request))
        response = self.get_response(request)
        return response
