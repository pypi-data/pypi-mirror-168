from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from .models import CustomGroup as Group

User = get_user_model()


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if not username:
                username = kwargs.get("email")
            user = User.objects.get(
                Q(mobile=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            User().set_password(password)
        except MultipleObjectsReturned:
            return User.objects.filter(
                Q(mobile=username) | Q(email__iexact=username)).order_by('id').first()
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def _get_group_permissions(self, user_obj):
        group_ids = user_obj.groups.values_list("id", flat=True)
        user_groups = Group.objects.filter(id__in=group_ids)
        perms = Permission.objects.none()
        if user_groups.exists():
            perms = user_groups.first().permissions.all()
        return perms

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active and super().has_perm(user_obj, perm, obj=obj)

