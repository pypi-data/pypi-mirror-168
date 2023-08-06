from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext as _
from fcm_django.models import FCMDevice

from . import models
from .models import CustomGroup
import cleverstack_auth.organisation.admin

admin.site.unregister(FCMDevice)
admin.site.unregister(Group)


@admin.register(ContentType)
class ContentTypeAdmin(admin.ModelAdmin):
    list_display = ["id", "app_label", "model"]
    search_fields = ["model", "app_label"]


@admin.register(models.BillingDetail)
class BillingDetailAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "name", "mobile", "country"]
    search_fields = ["user", "name"]


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'content_type', 'codename']
    list_display_links = ['id', 'name']
    search_fields = ['name', 'codename', 'content_type__model']


@admin.register(CustomGroup)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organisation', 'is_default']
    search_fields = ['name', 'organisation__name']
    list_display_links = ['id', 'name', 'organisation']
    autocomplete_fields = ['organisation', 'created_by']

    @admin.action(description="Make default")
    def make_default(self, request, queryset):
        try:
            queryset.update(is_default=True)
            self.message_user(request, "Selected groups marked as default.",
                              messages.SUCCESS)
        except Exception as error:
            self.message_user(request, str(error),
                              messages.ERROR)

    @admin.action(description="Remove default")
    def remove_default(self, request, queryset):
        try:
            queryset.update(is_default=False)
            self.message_user(request, "Selected groups removed from defaults.",
                              messages.SUCCESS)
        except Exception as error:
            self.message_user(request, str(error),
                              messages.ERROR)


@admin.register(models.User)
class UserAdmin(UserAdmin):
    list_display = (
        'id', 'email', 'username', 'mobile', 'get_groups', 'is_active'
    )
    list_display_links = ["id", "email", "username"]
    search_fields = ('email', 'mobile', 'username',)
    readonly_fields = ('date_joined', 'last_login')
    filter_horizontal = ('groups', 'user_permissions',)
    list_filter = ()
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {
            'fields': ('first_name', 'last_name', 'mobile', 'username')}),
        (
            _('Permissions'),
            {'fields': (
                'is_active', 'is_staff', 'is_org_staff', 'is_owner', 'is_customer', 'is_verified', 'is_accepted',
                'is_superuser',
                'groups', 'user_permissions'
            )}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )

    def get_groups(self, obj):
        return " | ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = "Groups"


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'org', 'role', 'branch', 'image', 'created_at']
    list_display_links = ['id', 'user']
    list_filter = ['created_at', 'updated_at', 'is_active', 'date_of_joining']
    autocomplete_fields = ['user', 'org', 'role', 'branch']
    search_fields = ['user__email', 'org__name', 'branch__name', 'role__name']


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'organisation', 'parent', 'share_data', 'is_default', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at', 'updated_at', 'share_data']
    autocomplete_fields = ['parent', 'organisation']
    search_fields = ['name', 'organisation__name', 'parent__name']
    actions = ["make_default", "remove_default"]

    @admin.action(description="Make default")
    def make_default(self, request, queryset):
        try:
            queryset.update(is_default=True)
            self.message_user(request, "Selected roles marked as default.",
                              messages.SUCCESS)
        except Exception as error:
            self.message_user(request, str(error),
                              messages.ERROR)

    @admin.action(description="Remove default")
    def remove_default(self, request, queryset):
        try:
            queryset.update(is_default=False)
            self.message_user(request, "Selected roles removed from defaults.",
                              messages.SUCCESS)
        except Exception as error:
            self.message_user(request, str(error),
                              messages.ERROR)


@admin.register(models.GenerateToken)
class ResetPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'created_at', 'ip_address', 'user_agent')
    search_fields = ('user__email',)

# @admin.register(FCMDevice)
# class FCMDeviceAdmin(admin.ModelAdmin):
#     list_display = ['id', 'type',
#                     'user', 'active', 'registration_id', 'date_created']
#     list_filter = ['active', 'type', 'date_created']
#     search_fields = ['name', 'user__email', 'registration_id']
#     actions = ["send_push_notification"]
#
#     @admin.action(description="Send test notification")
#     def send_push_notification(self, request, queryset):
#         try:
#             title = "testing FCM push notification"
#             body = "push notification body"
#             for device in queryset.filter(active=True):
#                 settings.PUSH_SERVICE.notify_single_device(
#                     registration_id=device.registration_id,
#                     message_title=title, message_body=body)
#             self.message_user(request, "Push notification has been sent to selected devices",
#                               messages.SUCCESS)
#         except Exception as error:
#             self.message_user(request, str(error),
#                               messages.ERROR)
