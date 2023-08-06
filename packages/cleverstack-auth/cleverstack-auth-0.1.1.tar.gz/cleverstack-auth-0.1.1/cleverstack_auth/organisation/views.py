from collections import OrderedDict

from cleverstack_auth.base.auth import AppBaseViewSet
from cleverstack_auth.models import Profile
from cleverstack_auth.utils.helpers import recursive_node_to_dict
from cleverstack_auth.utils.response import get_error_response, get_list_success_response, \
    get_create_success_response, get_update_success_response, get_no_permission_response, get_delete_success_response, \
    get_success_ok_response
from . import models
from . import serializers


# class OrganisationPlanViewSet(AppBaseViewSet):
#     queryset = models.OrganisationSubscription.objects.all()
#     serializer_class = serializers.OrganisationSubscriptionSerializer
#
#     def list(self, request, *args, **kwargs):
#         try:
#             queryset = self.filter_queryset(self.get_queryset().filter(organisation=request.org))
#             page = self.paginate_queryset(queryset)
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         except Exception as error:
#             return get_error_response(str(error))
#
#     def create(self, request, pk=None, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data, context={'request': request})
#             serializer.is_valid(raise_exception=True)
#             serializer.save(organisation=request.org)
#             return get_update_success_response("Subscription", serializer.data)
#         except Exception as error:
#             return get_error_response(str(error))


class BranchViewSet(AppBaseViewSet):
    queryset = models.Branch.objects.all()
    serializer_class = serializers.BranchSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset().filter(organisation=request.org))
            result = []
            for q in queryset:
                if not q.is_child_node():
                    data = recursive_node_to_dict(q)
                    result.append(data)
            ids = queryset.values_list("id", flat=True)
            if len(result) > 0:
                result[0]["id"] = "root"
            final_data = {
                "ids": set(ids),
                "data": result
            }
            return get_list_success_response("Branches", final_data)
        except Exception as error:
            return get_error_response(str(error))

    def create(self, request, pk=None, *args, **kwargs):
        try:
            data = OrderedDict()
            data.update(request.data)
            users = request.data.get("users")
            data["organisation"] = request.org.id
            parent = data.get("parent")
            if type(parent) == str and "root" in parent:
                root_branch = models.Branch.objects.filter(organisation=request.org, level=0).first()
                data["parent"] = root_branch.pk
            serializer = self.get_serializer(data=data, org=request.org)
            serializer.is_valid(raise_exception=True)
            branch = serializer.save()
            if users is not None:
                if len(users) > 0:
                    Profile.objects.filter(user_id__in=users).update(branch=branch)
            return get_create_success_response("Branch", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def update(self, request, *args, **kwargs):
        try:
            data = OrderedDict()
            data.update(request.data)
            users = request.data.get("users")
            data["organisation"] = request.org.id
            parent = data.get("parent")
            if type(parent) == str and "root" in parent:
                root_branch = models.Branch.objects.filter(organisation=request.org, level=0).first()
                data["parent"] = root_branch.pk
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            serializer = self.serializer_class(instance, data=data, partial=partial, org=request.org)
            serializer.is_valid(raise_exception=True)
            branch = serializer.save()
            existing_users = Profile.objects.filter(branch=instance).values_list("user", flat=True)
            if users is not None:
                Profile.objects.filter(user_id__in=existing_users).update(branch=None)
                Profile.objects.filter(user_id__in=users).update(branch=branch)
            return get_update_success_response("Note", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def destroy(self, request, *args, **kwargs):
        try:
            branch = self.get_object()
            if branch.organisation == request.org:
                if not branch.is_default:
                    super(BranchViewSet, self).destroy(request, *args, **kwargs)
                    return get_delete_success_response("Branch")
                return get_error_response("Default branch can not be deleted")
            return get_no_permission_response("You can not delete other organisation's branch")
        except Exception as error:
            return get_error_response(str(error))

    def retrieve(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.get_object())
            return get_success_ok_response("{} branch details fetched successfully".format(self.get_object().name),
                                           serializer.data)
        except Exception as error:
            return get_error_response(str(error))


class DepartmentViewSet(AppBaseViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset().filter(organisation=request.org))
            page = self.paginate_queryset(queryset)
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return get_error_response(str(error))

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data["organisation"] = request.org.pk
            users = request.data.get("users")
            branch = data.get("branch")
            if type(branch) == str and "root" in branch:
                root_branch = models.Branch.objects.filter(organisation=request.org, level=0).first()
                data["branch"] = root_branch.pk
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            department = serializer.save()
            if users is not None:
                Profile.objects.filter(user_id__in=users).update(department=department)
            return get_create_success_response("Branch Department", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            partial = kwargs.pop("partial", True)
            data = request.data.copy()
            branch = data.get("branch")
            users = data.get("users")
            if type(branch) == str and "root" in branch:
                root_branch = models.Branch.objects.filter(organisation=request.org, level=0).first()
                data["branch"] = root_branch.pk
            serializer = self.get_serializer(instance, data=data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            existing_users = Profile.objects.filter(department=instance).values_list("user", flat=True)
            if users is not None:
                Profile.objects.filter(user_id__in=existing_users).update(department=None)
                Profile.objects.filter(user_id__in=users).update(department=instance)
            return get_update_success_response("Branch Department", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.serializer_class(instance)
            return get_success_ok_response("Department details fetched successfully", serializer.data)
        except Exception as error:
            return get_error_response(str(error))

    def destroy(self, request, *args, **kwargs):
        try:
            department = self.get_object()
            if department.organisation == request.org:
                super(DepartmentViewSet, self).destroy(request, *args, **kwargs)
                return get_delete_success_response("Department")
            return get_no_permission_response("You can not delete other organisation's department")
        except Exception as error:
            return get_error_response(str(error))
