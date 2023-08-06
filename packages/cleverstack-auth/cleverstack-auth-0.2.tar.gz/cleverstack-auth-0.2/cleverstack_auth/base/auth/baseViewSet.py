import json

from django.http import QueryDict
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.serializers import ListSerializer, ModelSerializer

from cleverstack_auth.base.middleware import CustomResultsSetPagination
from .authentication import JSONWebTokenAuthentication


class CRUDPermission(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.user.is_owner:
            return True
        if request.method == "GET" and view.kwargs.get("pk"):
            perm = "{}.detail_{}".format(view.queryset.model._meta.app_label, view.queryset.model._meta.model_name)
            if request.user.has_perm(perm):
                return True
            return False
        return super(CRUDPermission, self).has_permission(request, view)


"""
    Admin Base View Set
"""


class AdminBaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JSONWebTokenAuthentication]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


"""
    App User ViewSet
"""


class CustomAuthenticated(IsAuthenticated):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        if request.org is None:
            raise serializers.ValidationError('org field is missing in the header')
        return bool(request.user and request.user.is_authenticated)


class AppBaseViewSet(viewsets.ModelViewSet):
    authentication_classes = [JSONWebTokenAuthentication]
    permission_classes = [CustomAuthenticated, CRUDPermission]
    pagination_class = CustomResultsSetPagination

    def transform_request_data(self, data):
        force_dict_data = data
        if type(force_dict_data) == QueryDict:
            force_dict_data = force_dict_data.dict()

        serializer = self.get_serializer()

        for key, value in serializer.get_fields().items():
            if isinstance(value, ListSerializer) or isinstance(value, ModelSerializer):
                if key in force_dict_data and type(force_dict_data[key]) == str:
                    if force_dict_data[key] == '':
                        force_dict_data[key] = None
                    else:
                        try:
                            force_dict_data[key] = json.loads(force_dict_data[key])
                        except:
                            pass
        return force_dict_data

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return super(AppBaseViewSet, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super(AppBaseViewSet, self).retrieve(request, *args, **kwargs)


"""
    ViewSet without token
"""


class BaseViewSet(viewsets.ModelViewSet):
    def create(self, request, *args, **kwargs):
        return super(BaseViewSet).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(BaseViewSet).update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super(BaseViewSet).destroy(request, *args, **kwargs)
