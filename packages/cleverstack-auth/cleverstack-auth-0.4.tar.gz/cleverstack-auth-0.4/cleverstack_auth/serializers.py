import re
from datetime import timedelta

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from fcm_django.models import FCMDevice
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer, \
    TokenRefreshSerializer, TokenObtainSerializer
from rest_framework_simplejwt.state import token_backend
from rest_framework_simplejwt.tokens import AccessToken

# from common.models import Address
# from common.serializers import AddressSerializer
from . import models
from .models import CustomGroup as Group

User = get_user_model()


class InviteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'mobile', 'email', 'groups', 'password']
        extra_kwargs = {'password': {'required': False, "write_only": True}}

    def to_representation(self, instance):
        data = super(InviteUserSerializer, self).to_representation(instance)
        groups = []
        if instance.user_profile:
            data['role'] = instance.user_profile.role.name
            data['alternate_phone'] = instance.user_profile.alternate_phone
            # data['address'] = AddressSerializer(
            #     instance.user_profile.address).data
        if instance.groups.exists():
            for group in instance.groups.all():
                groups.append(group.name)
            data["groups"] = groups
        return data


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Role
        fields = ["id", "name", "parent", "organisation", "is_default", "created_by", "created_at", "updated_at",
                  "share_data", "description"]

    def to_representation(self, instance):
        data = super(RoleSerializer, self).to_representation(instance)
        if instance.parent:
            data['parent'] = {"id": instance.parent.pk, "name": instance.parent.name}
        if instance.organisation:
            data['organisation'] = instance.organisation.name
        return data


class UserAuthenticationSerializer(TokenObtainPairSerializer, TokenObtainSerializer):

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'password': attrs['password'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        try:
            user = models.User.objects.get(email=authenticate_kwargs['email'])
            if not user.is_active:
                self.error_messages['no_active_account'] = _(
                    'Your account is not activated, contact your Organisation owner to activate it.'
                )
                raise exceptions.AuthenticationFailed(
                    self.error_messages['no_active_account'],
                    'no_active_account',
                )
        except models.User.DoesNotExist:
            self.error_messages['no_active_account'] = _(
                'Account does not exist')
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        self.user = authenticate(**authenticate_kwargs)
        if self.user is None:
            self.error_messages['no_active_account'] = _(
                'Incorrect Email, Mobile Number or Password')
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        data = super(UserAuthenticationSerializer, self).validate(attrs)
        data['user'] = self.user
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Inherit from `TokenRefreshSerializer` and touch the database
    before re-issuing a new access token and ensure that the user
    exists and is active.
    """

    error_msg = 'No active account found with the given credentials'

    def validate(self, attrs):
        token_payload = token_backend.decode(attrs['refresh'])
        try:
            user = get_user_model().objects.get(pk=token_payload['user_id'])
        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_account'
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_msg, 'no_active_account'
            )

        return super(CustomTokenRefreshSerializer, self).validate(attrs)


class UserSerializer(serializers.ModelSerializer):
    # address = AddressSerializer(write_only=True, required=False)

    def __init__(self, *args, **kwargs):
        self.org = kwargs.pop("org", None)
        super(UserSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile', 'first_name', 'last_name',
                  'password', 'groups', 'is_active', 'is_owner', 'is_org_staff', 'is_accepted']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5, 'required': False}}

    def validate_email(self, email):
        if self.instance:
            if self.instance.email != email:
                if not models.Profile.objects.filter(
                        user__email=email, org=self.org).exists():
                    return email
                raise serializers.ValidationError("Email already exists")
            return email
        else:
            if not models.Profile.objects.filter(user__email=email.lower(), org=self.org).exists():
                return email
            raise serializers.ValidationError('Given Email id already exists')

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        try:
            with transaction.atomic():
                user = get_user_model().objects.create_user(**validated_data)
                profile, created = models.Profile.objects.get_or_create(
                    user=user)
                if created:
                    profile.org = self.org
                    profile.date_of_joining = timezone.now()
                    profile.save()
        except Exception as error:
            raise error
        return user

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super(UserSerializer, self).update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user

    def to_representation(self, instance):
        data = super(UserSerializer, self).to_representation(instance)
        groups = []
        if instance.user_profile:
            data['role'] = {"id": instance.user_profile.role_id,
                            "name": instance.user_profile.role.name} if instance.user_profile.role else None
            data['branch'] = {"id": instance.user_profile.branch_id,
                              "name": instance.user_profile.branch.name} if instance.user_profile.branch else None
            data['image'] = instance.user_profile.image.url if instance.user_profile.image else None
            data['alternate_phone'] = instance.user_profile.alternate_phone
            # data['address'] = AddressSerializer(instance.user_profile.address).data
        for group in instance.groups.all():
            groups.append({"id": group.pk, "name": group.name})
        data["groups"] = groups
        return data


class ProfileSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField()
    # address = AddressSerializer()

    class Meta:
        model = models.Profile
        fields = ("phone", "alternate_phone", 'user_details', 'image', 'role', 'branch')

    def __init__(self, *args, **kwargs):
        super(ProfileSerializer, self).__init__(*args, **kwargs)
        self.fields["alternate_phone"].required = False
        # self.fields["role"].required = True
        self.fields["phone"].required = True

    @staticmethod
    def get_user_details(obj):
        return UserSerializer(obj.user).data

    def update(self, instance, validated_data):
        # address = validated_data.pop("address", None)
        # if address:
        #     address_obj, _ = Address.objects.update_or_create(
        #         address_users__id=instance.id, defaults=address)
        # else:
        #     address_obj = instance.address
        # instance.address = address_obj
        # instance.save()
        return super(ProfileSerializer, self).update(instance, validated_data)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get("email")
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise serializers.ValidationError(
                "You don't have an account. Please create one."
            )
        return data


class PasswordValidateMixin:

    @staticmethod
    def validate(data):
        token = data.get('token')
        password_reset_token_validation_time = models.get_password_reset_token_expiry_time()

        try:
            reset_password_token = _get_object_or_404(
                models.GenerateToken, key=token)
        except (TypeError, ValueError, ValidationError, Http404, models.GenerateToken.DoesNotExist):
            raise Http404(
                _("The OTP entered is not valid. Please check and try again."))

        expiry_date = reset_password_token.created_at + timedelta(
            hours=password_reset_token_validation_time)

        if timezone.now() > expiry_date:
            reset_password_token.delete()
            raise Http404(_("The tokens has expired"))
        return data


class ResetTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    token = serializers.CharField()


class PasswordTokenSerializer(PasswordValidateMixin, serializers.Serializer):
    password = serializers.CharField(label=_("Password"), style={
        'input_type': 'password'})
    token = serializers.CharField()


class PasswordSetSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)
    retype_password = serializers.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(PasswordSetSerializer, self).__init__(*args, **kwargs)

    def validate_old_password(self, pwd):
        if not check_password(pwd, self.context.get('user').password):
            raise serializers.ValidationError(
                "old password entered is incorrect.")
        return pwd

    def validate(self, data):
        if len(data.get('new_password')) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long!")
        if data.get('new_password') == data.get('old_password'):
            raise serializers.ValidationError(
                "New_password and old password should not be the same")
        if data.get('new_password') != data.get('retype_password'):
            raise serializers.ValidationError(
                "New_password and Retype_password did not match.")
        return data


def find_urls(string):
    website_regex = "^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,63}$"
    website_regex_port = "^https?://[A-Za-z0-9.-]+\.[A-Za-z]{2,63}:[0-9]{2,4}$"
    url = re.findall(website_regex, string)
    url_port = re.findall(website_regex_port, string)
    if url and url[0] != "":
        return url
    return url_port


class APISettingsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(APISettingsSerializer, self).__init__(*args, **kwargs)

    class Meta:
        model = models.APISettings
        fields = ("title", "website")

    @staticmethod
    def validate_website(website):
        if website and not (website.startswith("http://") or website.startswith("https://")):
            raise serializers.ValidationError("Please provide valid schema")
        if not len(find_urls(website)) > 0:
            raise serializers.ValidationError(
                "Please provide a valid URL with schema and without trailing slash - Example: https://google.com"
            )
        return website


class UserTokenVerifySerializer(TokenVerifySerializer):
    def validate(self, attrs):
        data = super(UserTokenVerifySerializer, self).validate(attrs)
        access_token_obj = AccessToken(attrs['token'])
        user_id = access_token_obj['user_id']
        user = User.objects.get(id=user_id)
        data['user_role'] = user.user_profile.role
        data['user'] = user
        return data


class GroupSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'description', 'created_by', 'created_at', 'updated_at', 'is_default']

    @staticmethod
    def get_created_by(obj):
        if obj.created_by:
            return obj.created_by.email
        return None


class FCMDeviceSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = FCMDevice
        fields = ['id', 'user', 'active', 'registration_id', 'date_created']

    @staticmethod
    def get_user(obj):
        return obj.user.email


class BillingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillingDetail
        fields = ["id", "organisation", "user", "name", "mobile", "country", "city", "state", "street_address",
                  "zip_code"]

    def create(self, validated_data):
        billing_detail, created = models.BillingDetail.objects.get_or_create(**validated_data)
        return billing_detail
