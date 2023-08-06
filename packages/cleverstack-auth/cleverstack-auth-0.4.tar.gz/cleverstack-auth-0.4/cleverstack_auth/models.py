import datetime

import arrow
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group, Permission
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import PermissionDenied
from django.contrib import auth
from sendgrid import Mail

from cleverstack_auth.base import tokens
from cleverstack_auth.base.models import BaseModel
from cleverstack_auth.organisation.models import Organisation
from cleverstack_auth import signals


class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email=self.normalize_email(
            email), password=password, **kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_verified = True
        user.save(using=self._db)
        org, _ = Organisation.objects.get_or_create(name="TechnoDreams")
        role, created = Role.objects.get_or_create(name="Owner", organisation=org)
        Profile.objects.create(user=user, role=role, org=org)
        return user


# A few helper functions for common logic between User and AnonymousUser.
def _user_get_permissions(user, obj, from_name):
    permissions = set()
    name = 'get_%s_permissions' % from_name
    for backend in auth.get_backends():
        if hasattr(backend, name):
            permissions.update(getattr(backend, name)(user, obj))
    return permissions


def _user_has_perm(user, perm, obj):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_perm'):
            continue
        try:
            if backend.has_perm(user, perm, obj):
                return True
        except PermissionDenied:
            return False
    return False


def _user_has_module_perms(user, app_label):
    """
    A backend can raise `PermissionDenied` to short-circuit permission checking.
    """
    for backend in auth.get_backends():
        if not hasattr(backend, 'has_module_perms'):
            continue
        try:
            if backend.has_module_perms(user, app_label):
                return True
        except PermissionDenied:
            return False
    return False


class PermissionsMixin(models.Model):
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    groups = models.ManyToManyField(
        "CustomGroup",
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_permissions",
        related_query_name="user",
    )

    class Meta:
        abstract = True

    def get_user_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'user')

    def get_group_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'group')

    def get_all_permissions(self, obj=None):
        return _user_get_permissions(self, obj, 'all')

    def has_perm(self, perm, obj=None):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    # Personal Info
    username = models.CharField(max_length=256, verbose_name=_("Username"), blank=True, null=True)
    email = models.EmailField(verbose_name=_("Email"), max_length=60, unique=True)
    first_name = models.CharField(max_length=256, verbose_name=_("First Name"), blank=True, null=True)
    last_name = models.CharField(max_length=256, verbose_name=_("Last Name"), blank=True, null=True)
    mobile = PhoneNumberField(null=True, unique=True, blank=True, verbose_name=_("Mobile Number"))
    # extra fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_org_staff = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_reseller = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_user", "Access"),
            ("detail_user", "View"),
            ("view_user", "List"),
            ("change_user", "Edit"),
            ("delete_user", "Delete"),
            ("add_user", "Create"),
        )

    def save(self, *args, **kwargs):
        if not self.username:
            if self.email:
                self.username = self.email.split("@")[0]
            else:
                self.username = self.mobile
        if self.is_owner:
            self.is_customer = False
            self.is_org_staff = False
        elif self.is_org_staff:
            self.is_customer = False
            self.is_owner = False
        elif self.is_customer:
            self.is_org_staff = False
            self.is_owner = False
        if self.is_owner and self.is_org_staff:
            self.is_org_staff = False
            self.is_customer = False
        if self.is_org_staff and self.is_customer:
            self.is_owner = False
            self.is_customer = False
        if self.is_owner and self.is_customer:
            self.is_org_staff = False
            self.is_customer = False
        return super(User, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.email)

    @property
    def get_short_name(self):
        return self.username

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            full_name = "{} {}".format(
                str(self.first_name), str(self.last_name))
        elif self.first_name and not self.last_name:
            full_name = self.first_name
        elif self.last_name and not self.first_name:
            full_name = self.last_name
        elif self.username:
            full_name = self.username
        else:
            full_name = self.email
        return full_name

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    @property
    def created_on_arrow(self):
        return arrow.get(self.date_joined).humanize()

    @property
    def image(self):
        return self.user_profile.image.url if self.user_profile.image else ""


class Role(MPTTModel, BaseModel):
    name = models.CharField(max_length=100)
    organisation = models.ForeignKey("cleverstack_auth.Organisation", null=True, on_delete=models.CASCADE, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    share_data = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    class Meta:
        default_permissions = []
        ordering = ["-created_at"]
        permissions = (
            ("access_role", "Access"),
            ("detail_role", "View"),
            ("view_role", "List"),
            ("change_role", "Edit"),
            ("delete_role", "Delete"),
            ("add_role", "Create"),
        )

    def __str__(self) -> str:
        return "{} : {}".format(self.id, self.name)


class Profile(BaseModel):
    """ this model is used for activating the user within a particular expiration time """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_profile")
    image = models.ImageField(upload_to="user_images", null=True, blank=True)
    org = models.ForeignKey("cleverstack_auth.Organisation", null=True, on_delete=models.CASCADE, blank=True)
    branch = models.ForeignKey("cleverstack_auth.Branch", null=True, on_delete=models.SET_NULL, blank=True)
    department = models.ForeignKey("cleverstack_auth.Department", null=True, on_delete=models.SET_NULL, blank=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="user_role")
    phone = PhoneNumberField(null=True, unique=True, blank=True)
    alternate_phone = PhoneNumberField(null=True, blank=True)
    # address = models.ForeignKey("common.Address", related_name="address_users", on_delete=models.SET_NULL, blank=True,
    #                             null=True)
    is_active = models.BooleanField(default=True)
    date_of_joining = models.DateField(null=True, blank=True, auto_now_add=True)
    activation_key = models.CharField(max_length=150, null=True, blank=True)
    key_expires = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.email

    class Meta:
        unique_together = (("user", "org"),)
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_profile", "Access"),
            ("detail_profile", "View"),
            ("view_profile", "List"),
            ("change_profile", "Edit"),
            ("delete_profile", "Delete"),
            ("add_profile", "Create"),
        )

    def save(self, *args, **kwargs):
        """ by default the expiration time is set to 2 hours """
        self.key_expires = timezone.now() + datetime.timedelta(hours=2)
        super(Profile, self).save(*args, **kwargs)

    # @property
    # def is_admin(self):
    #     return self.is_organization_admin


class CustomGroup(BaseModel):
    name = models.CharField(_('name'), max_length=150, blank=True, null=True)
    permissions = models.ManyToManyField(Permission, verbose_name=_('permissions'), blank=True,
                                         related_name="permissions")
    default_permissions = models.ManyToManyField(Permission, blank=True, related_name="default_permissions")
    organisation = models.ForeignKey("cleverstack_auth.Organisation", on_delete=models.CASCADE, null=True, blank=True,
                                     related_name="org_groups")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name="groups_created_by")
    description = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_customgroup", "Access"),
            ("detail_customgroup", "View"),
            ("view_customgroup", "List"),
            ("change_customgroup", "Edit"),
            ("delete_customgroup", "Delete"),
            ("add_customgroup", "Create"),
        )

    def __str__(self):
        return "{} : {}".format(self.id, self.name)


TOKEN_GENERATOR_CLASS = tokens.get_token_generator()


class GenerateToken(BaseModel):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='custom_password_reset_tokens', on_delete=models.CASCADE,
                             verbose_name=_("The User which is associated to this password reset tokens"))
    key = models.CharField(_("Key"), max_length=64, db_index=True, unique=True)
    ip_address = models.GenericIPAddressField(
        _("The IP address of this session"), default="", blank=True, null=True, )
    user_agent = models.CharField(max_length=256, verbose_name=_(
        "HTTP User Agent"), default="", blank=True, )

    class Meta:
        verbose_name = _("Password Reset Token")
        ordering = ["-created_at"]
        verbose_name_plural = _("Password Reset Tokens")
        default_permissions = []
        permissions = (
            ("access_generatetoken", "Access"),
            ("detail_generatetoken", "View"),
            ("view_generatetoken", "List"),
            ("change_generatetoken", "Edit"),
            ("delete_generatetoken", "Delete"),
            ("add_generatetoken", "Create"),
        )

    @staticmethod
    def generate_key():
        """ generates a pseudo random code using os.urandom and binascii.hexlify """
        token = TOKEN_GENERATOR_CLASS.generate_token()
        return token

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(GenerateToken, self).save(*args, **kwargs)

    def __str__(self):
        return "Password reset tokens for user {user}".format(user=self.user)


@receiver(signals.reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email = reset_password_token.user.email
    subject = "OTP to reset your CleverStack account password"
    messages = f'{reset_password_token.key} is your otp to reset your password. CleverStack'
    template_id = getattr(settings, 'TEMPLATE_ID', '123456789')
    message = Mail(
        from_email='support@cleverstack.in',
        to_emails=email,
        subject=subject,
        plain_text_content=messages)
    client = getattr(settings, "SEND_GRID_CLIENT")
    client.send(message)


def get_password_reset_token_expiry_time():
    return getattr(settings, 'DJANGO_REST_MULTI_TOKEN_AUTH_RESET_TOKEN_EXPIRY_TIME', 24)


def get_password_reset_lookup_field():
    return getattr(settings, 'DJANGO_REST_LOOKUP_FIELD', 'email')


def clear_expired(expiry_time):
    GenerateToken.objects.filter(created_at__lte=expiry_time).delete()


def eligible_for_reset(self):
    if not self.is_active:
        return False

    if getattr(settings, 'DJANGO_REST_MULTI_TOKEN_AUTH_REQUIRE_USABLE_PASSWORD', True):
        return self.has_usable_password()
    else:
        return True


User.add_to_class("eligible_for_reset", eligible_for_reset)


class APISettings(BaseModel):
    title = models.CharField(max_length=1000)
    apikey = models.CharField(max_length=16, blank=True)
    website = models.URLField(max_length=255, default="")
    lead_assigned_to = models.ManyToManyField(
        User, related_name="lead_assignee_users")
    created_by = models.ForeignKey(
        User, related_name="settings_created_by", on_delete=models.SET_NULL, null=True)
    org = models.ForeignKey("cleverstack_auth.Organisation",
                            blank=True, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_apisettings", "Access"),
            ("detail_apisettings", "View"),
            ("view_apisettings", "List"),
            ("change_apisettings", "Edit"),
            ("delete_apisettings", "Delete"),
            ("add_apisettings", "Create"),
        )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.apikey or self.apikey is None or self.apikey == "":
            self.apikey = tokens.generate_key()
        super(APISettings, self).save(*args, **kwargs)


class BillingDetail(BaseModel):
    organisation = models.ForeignKey("cleverstack_auth.Organisation", on_delete=models.CASCADE)
    user = models.ForeignKey("cleverstack_auth.User", on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="user_billing_details")
    name = models.CharField(max_length=255, null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
