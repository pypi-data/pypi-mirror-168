from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from cleverstack_auth.models import Organisation, Profile
from threading import local


def set_profile_request(request, org):
    if request.user.is_authenticated:
        request.profile = Profile.objects.filter(
            user=request.user, org=org, is_active=True).first()
        if request.profile is None:
            logout(request)
            return Response(
                {"error": False}, status=status.HTTP_200_OK,
            )


class GetOrganisation(object):
    _thread_locals = local()

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    @staticmethod
    def process_request(request):
        org = None
        if request.user.is_authenticated:
            org = request.user.user_profile.org.name
        GetOrganisation._thread_locals.org = org


class GetProfileAndOrg(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        if request.headers.get("org"):
            org_id = request.headers.get("org")
            org = Organisation.objects.filter(id=org_id).first()
            if org:
                request.org = org
                set_profile_request(request, org)
            else:
                request.org = None
        else:
            request.org = None
