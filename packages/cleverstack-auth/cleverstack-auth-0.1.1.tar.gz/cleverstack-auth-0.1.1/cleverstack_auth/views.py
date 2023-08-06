import json
import threading
from collections import OrderedDict
from datetime import timedelta

import arrow
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from dj_rest_auth.registration.views import SocialLoginView
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.password_validation import validate_password, get_password_validators
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.expressions import Q
from django.shortcuts import render
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from fcm_django.models import FCMDevice
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenObtainPairView, TokenVerifyView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from cleverstack_auth.base.auth import BaseViewSet, AppBaseViewSet
from cleverstack_auth.organisation.models import Organisation, Branch
from cleverstack_auth.organisation.serializers import OrganizationSerializer, CheckOrganisationSerializer
# from subscription.models import Subscription, SubscriptionCycle
from cleverstack_auth.utils.helpers import send_otp_via_email, get_login_info, send_email, recursive_node_to_dict, get_ip_and_user_agent
from cleverstack_auth.utils.response import *
from . import models
from . import serializers
from . import signals
from .models import CustomGroup as Group, GenerateToken, CustomGroup
from .serializers import CustomTokenRefreshSerializer

User = get_user_model()

HTTP_USER_AGENT_HEADER = getattr(
    settings, 'DJANGO_REST_PASSWORD_RESET_HTTP_USER_AGENT_HEADER', 'HTTP_USER_AGENT')
HTTP_IP_ADDRESS_HEADER = getattr(
    settings, 'DJANGO_REST_PASSWORD_RESET_IP_ADDRESS_HEADER', 'REMOTE_ADDR')


class IndexView(TemplateView):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {})

# class FacebookLogin(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
#
#
# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter


class ValidateOrganisationViewSet(BaseViewSet):
    queryset = Organisation.objects.all()
    serializer_class = CheckOrganisationSerializer
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({
                "message": "OK",
                "error": False
            }, status=status.HTTP_200_OK)
        except Exception as error:
            return get_error_response(error.args[0])


class OrganisationViewSet(BaseViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ('name',)
    http_method_names = ["post"]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            org_name = request.data.get('name')
            email = request.data.get('email')
            mobile = request.data.get('mobile')
            first_name = request.data.get('first_name', "")
            last_name = request.data.get('last_name', "")
            password = request.data.get('password')
            serializer.is_valid(raise_exception=True)
            with transaction.atomic():
                user, created = User.objects.get_or_create(email=email)
                if created:
                    user.mobile = mobile
                    user.is_owner = True
                    user.first_name = first_name
                    user.last_name = last_name
                    user.set_password(password)
                    user.save()
                    org, _ = models.Organisation.objects.get_or_create(name=org_name.lower())
                    role = models.Role.objects.create(name="CEO", organisation=org, created_by_id=user.id, share_data=False,
                                                      is_default=True)
                    models.Role.objects.create(name="Manager", organisation=org, created_by=user, share_data=False,
                                               is_default=True)
                    branch, created = Branch.objects.get_or_create(name=org_name, organisation=org, manager=user,
                                                                   is_default=True)
                    profile, _ = models.Profile.objects.get_or_create(user=user, org=org, role=role, branch=branch)
                    profile.is_organization_admin = True
                    profile.save()
                    admin, _ = CustomGroup.objects.get_or_create(organisation=user.user_profile.org,
                                                                 name="Administrator", is_default=True)
                    perms = Permission.objects.values_list("id", flat=True)
                    admin.permissions.set(perms)
                    user.groups.add(admin)
                    send_otp_via_email(user, request)
                    headers = self.get_success_headers(serializer.data)
                    user_info = get_login_info(user, request)
                    return Response({
                        "data": user_info,
                        "error": False,
                        "message": "Organisation created Successfully.",
                    }, status=status.HTTP_200_OK, headers=headers)
                return get_success_response("User already Exists, Please login to check the account.")
        except Exception as error:
            return get_error_response(error.args[0])


class UserActivateView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        try:
            otp = request.data.get("otp")
            user_id = request.data.get("user_id")
            if otp:
                otp_key = GenerateToken.objects.filter(key=otp, user_id=user_id)
                if otp_key.exists():
                    key = otp_key.first()
                    time_diff = timezone.now() - key.created_at
                    if time_diff.seconds / 60 > 5:
                        key.delete()
                        return get_error_response("This otp is expired")
                    user = key.user
                    user.is_verified = True
                    user.save()
                    modules = ContentType.objects.filter(model__in=["ticket", "lead", "contact", "account"]
                                                         ).values_list("id", flat=True)
                    subscription, _ = Subscription.objects.get_or_create(name="Trial", max_storage=2,
                                                                         is_trial=True, is_free=True)
                    subscription.modules.set(modules)
                    subscription_cycle, _ = SubscriptionCycle.objects.get_or_create(name="Monthly", price=0,
                                                                                    interval=15,
                                                                                    subscription=subscription)
                    expiration_date = arrow.now().shift(days=subscription_cycle.interval)
                    OrganisationSubscription.objects.create(organisation=user.user_profile.org,
                                                            cycle=subscription_cycle, subscription=subscription,
                                                            purchase_date=timezone.now(), users=10, amount=0,
                                                            expire_date=str(expiration_date))
                    key.delete()
                    return get_success_ok_response("Account verified successfully", "")
                return get_error_response("Invalid/Wrong otp")
            return get_error_response("otp is missing in body")
        except Exception as error:
            return get_error_response(str(error))


class NewOtpView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            user = User.objects.get(pk=user_id)
            thread = threading.Thread(target=send_otp_via_email, args=(user, request),
                                      daemon=True)
            thread.start()
            return get_success_ok_response("OTP re-sent successfully.", "")
        except Exception as error:
            return get_error_response(str(error))


class UserAuthenticationView(TokenObtainPairView):
    serializer_class = serializers.UserAuthenticationSerializer

    def post(self, request, *args, **kwargs):
        try:
            super(UserAuthenticationView, self).post(request, *args, **kwargs)
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            # permissions = Permission.objects.filter().values_list("id", flat=True)
            # for pk in permissions:
            #     user.user_permissions.add(pk)
            return get_success_ok_response("User Authenticated Successfully.", get_login_info(user, request))
        except Exception as error:
            return get_error_response(str(error))


class CustomTokenRefreshView(TokenRefreshView):
    """
    Refresh token generator view.
    """

    serializer_class = CustomTokenRefreshSerializer


class UserViewSet(AppBaseViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'email': ['exact', 'iexact', 'contains', 'icontains'],
        'username': ['exact', 'iexact', 'contains', 'icontains'],
        'first_name': ['exact', 'iexact', 'contains', 'icontains'],
        'last_name': ['exact', 'iexact', 'contains', 'icontains'],
        'mobile': ['exact', 'iexact', 'contains', 'icontains'],
        'is_active': ['exact', 'iexact', 'contains', 'icontains'],
        'is_verified': ['exact', 'iexact', 'contains', 'icontains'],
        'created_at': ['gt', 'lt', 'lte', 'gte', 'exact', 'iexact', 'contains', 'icontains'],
        'updated_at': ['gt', 'lt', 'lte', 'gte', 'exact', 'iexact', 'contains', 'icontains'],
    }

    def list(self, request, *args, **kwargs):
        try:
            org_users = []
            org_profile_users = models.Profile.objects.filter(org=request.org).values_list("user", flat=True)
            queryset = self.queryset.filter(id__in=org_profile_users)
            remaining_users = 0
            # org_subscription = OrganisationSubscription.objects.filter(organisation=request.org)
            # if org_subscription.exists():
            #     remaining_users = org_subscription.first().subscription.employees - queryset.count()
            if request.user.is_owner:
                org_users = models.Profile.objects.filter(
                    Q(user__is_org_staff=True) |
                    Q(user__is_owner=True), org=request.org).values_list("user", flat=True)
            else:
                org_users = models.Profile.objects.filter(
                    Q(user__is_org_staff=True) |
                    Q(user__is_owner=True),
                    Q(role__parent=request.user.user_profile.role) |
                    Q(role=request.user.user_profile.role),
                    Q(branch=request.user.user_profile.branch) |
                    Q(branch__parent=request.user.user_profile.branch),
                    org=request.org).values_list('user', flat=True)
            queryset = self.filter_queryset(self.queryset.filter(id__in=org_users))
            page = self.paginate_queryset(queryset)
            serializer = self.get_serializer(page, org=request.org,
                                             context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return get_error_response(str(error))

    def create(self, request, *args, **kwargs):
        try:
            org_profile_users = models.Profile.objects.filter(org=request.org).values_list("user", flat=True)
            queryset = self.queryset.filter(id__in=org_profile_users)
            # org_subscription = OrganisationSubscription.objects.filter(organisation=request.org, is_active=True)
            users = 0
            subscription_plan = None
            # if org_subscription.exists():
            #     if org_subscription.filter(Q(subscription__is_trial=True) & Q(subscription__is_trial=False)).exists():
            #         subscription_plan = org_subscription.filter(subscription__is_trial=False).first()
            #         users = org_subscription.filter(subscription__is_trial=False).first().users
            #     elif org_subscription.filter(subscription__is_trial=True).exists():
            #         subscription_plan = org_subscription.first()
            #         users = org_subscription.first().subscription.employees
            #     elif org_subscription.filter(subscription__is_trial=False).exists():
            #         subscription_plan = org_subscription.first()
            #         users = org_subscription.first().users
            # else:
            #     return get_error_response("No trial period or subscription availed")
            # if queryset.count() >= users:
            #     return get_error_response("Users limit is {} based on your {}".format(
            #         users, "Trial period" if subscription_plan.subscription.is_trial else "Subscription plan"))
            groups = request.data.get("groups")
            password = request.data.get("password")
            role = request.data.get("role")
            branch = request.data.get("branch")
            if type(branch) == str and "root" in branch:
                branch = Branch.objects.filter(organisation=request.org, level=0).first().id
            if type(role) == str and "root" in role:
                role = models.Role.objects.filter(organisation=request.org, level=0).first().id
            with transaction.atomic():
                serializer = serializers.InviteUserSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                user.is_org_staff = True
                user.is_active = False
                user.save()
                user.groups.set(groups)
                models.Profile.objects.create(org=request.org, user=user, role_id=role, branch_id=branch)
                if password:
                    user.is_verified = True
                    user.is_accepted = True
                    user.set_password(password)
                    user.save()
                else:
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = RefreshToken.for_user(user)

                    url = "https://cleverstack-frontend.vercel.app/account/activate/{}".format(token.access_token)
                    message = "Hello {}, " \
                              "\n " \
                              "\n {} has invited you to join CleverStack CRM account. " \
                              "\n Please copy and paste the following address into your browser. " \
                              "\n {}" \
                              "\n " \
                              "\nRegards, \nCleverStack CRM Team".format(user.get_full_name, request.user.get_full_name,
                                                                         url)

                    subject = "You are invited to join {}'s CleverStack CRM account".format(
                        request.user.get_full_name)
                    thread = threading.Thread(target=send_email, args=(user.email, subject, message),
                                              daemon=True)
                    thread.start()
                return get_success_ok_response("User added successfully", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def update(self, request, *args, **kwargs):
        try:
            role = request.data.get("role")
            branch = request.data.get("branch")
            data = request.data.copy()
            if type(branch) == str and "root" in branch:
                data["branch"] = Branch.objects.filter(organisation=request.org, level=0).first().id
            if type(role) == str and "root" in role:
                data["role"] = models.Role.objects.filter(organisation=request.org, level=0).first().id
            user_serializer = self.serializer_class(self.get_object(), data=request.data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            profile = models.Profile.objects.get(user_id=self.get_object().id)
            profile_serializer = serializers.ProfileSerializer(profile, data=data, partial=True)
            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()
            return get_success_ok_response("User updated successfully", user_serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    @action(methods=['post'], detail=True, url_path='change-password')
    def set_password(self, request, pk=None):
        serializer = serializers.PasswordSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.User.objects.get(mobile=pk)
        user.set_password(request.data['password'])
        user.save()
        return get_success_ok_response("successfully reset password.", None)

    @action(detail=False, methods=['post'], url_path='deactivate')
    def deactivate_users(self, request, *args, **kwargs):
        try:
            users = request.data.get("users")
            is_active = request.data.get("is_active")
            if users and is_active is not None:
                owners = models.User.objects.filter(is_owner=True).values_list("id", flat=True)
                for user in users:
                    if user in owners:
                        users.remove(user)
                models.User.objects.filter(id__in=users).update(is_active=is_active)
                return get_success_response(
                    "Users {} successfully".format("activated" if is_active else "deactivated"))
            return get_error_response("users or is_active is missing in body")
        except Exception as error:
            return get_error_response(str(error))

    @action(detail=False, methods=['post'], url_path='bulk_delete')
    def bulk_delete(self, request):
        try:
            users = request.data.get("users")
            if users:
                owners = models.User.objects.filter(is_owner=True).values_list("id", flat=True)
                for user in users:
                    if user in owners:
                        users.remove(user)
                models.User.objects.filter(id__in=users).delete()
                return get_success_ok_response("Selected users deleted successfully", "")
            return get_error_response("users is missing in body")
        except Exception as error:
            return get_error_response(str(error))

    @action(detail=False, methods=['get'], url_path='limit')
    def get_user_limit(self, request, *args, **kwargs):
        try:
            organisation_plan = OrganisationSubscription.objects.filter(organisation=request.org, is_active=True)
            organisation_users = models.Profile.objects.filter(org=request.org).count()
            remaining_users = 0
            total_users = 0
            if organisation_plan.exists():
                if organisation_plan.filter(Q(subscription__is_trial=True) & Q(subscription__is_trial=False)).exists():
                    total_users = organisation_plan.filter(subscription__is_trial=False).first().users
                elif organisation_plan.filter(subscription__is_trial=True).exists():
                    total_users = organisation_plan.first().subscription.employees
                elif organisation_plan.filter(subscription__is_trial=False).exists():
                    total_users = organisation_plan.first().users
                remaining_users = total_users - organisation_users
                data = {
                    "total_users": total_users,
                    "users": organisation_users,
                    "remaining_users": remaining_users
                }
                return get_success_ok_response("User limit fetched successfully.", data)
        except Exception as error:
            return get_error_response(str(error))
    
    @action(detail=False, methods=['post'], url_path='re_invite')
    def re_invite_users(self, request, *args, **kwargs):
        try:
            user_id = request.data.get("user_id")
            user = models.User.objects.get(id=user_id)
            token = RefreshToken.for_user(user)
            url = "https://cleverstack-frontend.vercel.app/account/activate/{}".format(token.access_token)
            message = "Hello {}, " \
                        "\n " \
                        "\n {} has invited you to join CleverStack CRM account. " \
                        "\n Please copy and paste the following address into your browser. " \
                        "\n {}" \
                        "\n " \
                        "\nRegards, \nCleverStack CRM Team".format(user.get_full_name, request.user.get_full_name,
                                                                    url)

            subject = "You are invited to join {}'s CleverStack CRM account (resent)".format(
                request.user.get_full_name)
            thread = threading.Thread(target=send_email, args=(user.email, subject, message),
                                        daemon=True)
            thread.start()
            return get_success_response("Invitation re-sent successfully")
        except Exception as error:
            return get_error_response(error.args)


class InviteUserViewSet(GenericAPIView):
    serializer_class = serializers.UserSerializer
    queryset = models.User.objects.all()
    authentication_classes = []
    http_method_names = ["get", "post"] 

    def get(self, request, *args, **kwargs):
        try:
            token = kwargs.get("token")
            try:
                access_token_obj = AccessToken(token)
                user_id = access_token_obj['user_id']
                user = User.objects.get(id=user_id)
                serializer = self.serializer_class(user)
                return get_success_ok_response("User details fetched successfully", serializer.data)
                # user_id = urlsafe_base64_decode(uid).decode()
                # user = User.objects.get(pk=user_id)
            except (TypeError, ValueError, TokenError, User.DoesNotExist):
                return get_error_response("Invitation expired or invalid link")
            # if user and default_token_generator.check_token(user, token):
            #     serializer = self.serializer_class(user)
            #     return get_success_ok_response("User details fetched successfully", serializer.data)
            # return get_error_response("Invitation expired or invalid link")
        except Exception as error:
            return get_error_response(str(error))
    
    def post(self, request, *args, **kwargs):
        try:
            uid = request.data.get("uid")
            token = kwargs.get("token")
            password = request.data.get("password")
            if password:
                try:
                    # user_id = urlsafe_base64_decode(uid).decode()
                    # user = User.objects.get(pk=user_id)
                    access_token_obj = AccessToken(token)
                    user_id = access_token_obj['user_id']
                    user = User.objects.get(id=user_id)
                    user.is_verified = True
                    user.is_accepted = True
                    user.is_active = True
                    user.set_password(password)
                    user.save()
                    return get_success_ok_response("User created successfully", get_login_info(user, request))
                except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                    return get_error_response("Invitation expired or invalid link")
                # if user and default_token_generator.check_token(user, token):
                #     user.is_verified = True
                #     user.is_accepted = True
                #     user.is_active = True
                #     user.set_password(password)
                #     user.save()
                #     return get_success_ok_response("User created successfully", get_login_info(user, request))
                # return get_error_response("Invitation expired or invalid link")
            return get_error_response("Please set a password to complete your account.")
        except Exception as error:
            return get_error_response(str(error))


class ResetPasswordValidateToken(GenericAPIView):
    serializer_class = serializers.ResetTokenSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({'status': 'OK'})
        except Exception as error:
            return get_error_response(str(error))


class UserTokenVerifyView(TokenVerifyView):
    serializer_class = serializers.UserTokenVerifySerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            user = None
            try:
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data.get("user")
            except TokenError as e:
                return Response({
                    "message": "Token is invalid or Expired",
                    "error": True
                }, status=401)
            return get_list_success_response("User Info", get_login_info(user, request))
        except Exception as error:
            return get_error_response(str(error))


class ResetPasswordConfirm(GenericAPIView):
    serializer_class = serializers.PasswordTokenSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            password = serializer.validated_data['password']
            token = serializer.validated_data['token']

            reset_password_token = models.GenerateToken.objects.filter(
                key=token).first()

            if reset_password_token.user.eligible_for_reset():
                signals.pre_password_reset.send(
                    sender=self.__class__, user=reset_password_token.user)
                try:
                    validate_password(password, user=reset_password_token.user,
                                      password_validators=get_password_validators(settings.AUTH_PASSWORD_VALIDATORS))
                except ValidationError as e:
                    raise exceptions.ValidationError({'password': e.messages})

                reset_password_token.user.set_password(password)
                reset_password_token.user.save()
                signals.post_password_reset.send(
                    sender=self.__class__, user=reset_password_token.user)

            models.GenerateToken.objects.filter(
                user=reset_password_token.user).delete()

            return get_success_response("Password updated successfully.")
        except Exception as error:
            return get_error_response(str(error))


class ResetPasswordRequestToken(GenericAPIView):
    serializer_class = serializers.ForgotPasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data['email']

            password_reset_token_validation_time = models.get_password_reset_token_expiry_time()
            now_minus_expiry_time = timezone.now(
            ) - timedelta(hours=password_reset_token_validation_time)
            models.clear_expired(now_minus_expiry_time)

            users = User.objects.filter(
                **{'{}__iexact'.format(models.get_password_reset_lookup_field()): email})
            active_user_found = False

            for user in users:
                if user.eligible_for_reset():
                    active_user_found = True

            if not active_user_found and not getattr(settings, 'DJANGO_REST_PASSWORD_RESET_NO_INFORMATION_LEAKAGE',
                                                     False):
                raise exceptions.ValidationError({
                    'email': [_(
                        "We couldn't find an account associated with that email. Please try a different email.")],
                })

            for user in users:
                if user.eligible_for_reset():
                    if user.custom_password_reset_tokens.all().count() > 0:
                        token = user.custom_password_reset_tokens.all()[0]
                    else:
                        ip, agent = get_ip_and_user_agent(request)
                        token = models.GenerateToken.objects.create(
                            user=user,
                            user_agent=agent,
                            ip_address=ip,
                        )
                    signals.reset_password_token_created.send(sender=self.__class__, instance=self,
                                                              reset_password_token=token)
            return get_success_response("OTP sent to Registered Email Address")
        except Exception as error:
            return get_error_response(error.args)


class DeviceTokenAPIView(AppBaseViewSet):
    queryset = FCMDevice.objects.all()
    serializer_class = serializers.FCMDeviceSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        try:
            device_token = request.data.get("device_token", None)
            if device_token:
                device, _ = FCMDevice.objects.get_or_create(
                    registration_id=device_token, user_id=request.user.id)
                return get_success_ok_response("Device token saved successfully.", self.serializer_class(device).data)
            else:
                return get_error_response("device_token is missing in body")
        except Exception as error:
            return get_error_response(str(error))

    @action(methods=['post'], detail=False, url_path="handle")
    def handle_device(self, request):
        try:
            token = request.data.get("token", None)
            active = request.data.get("active", None)
            if (token and active) is not None:
                if FCMDevice.objects.filter(registration_id=token, user=request.user).exists():
                    device = FCMDevice.objects.get(
                        registration_id=token, user=request.user)
                    device.active = json.loads(active)
                    device.save()
                    message = "Push notifications are turned on" if json.loads(
                        active) else "Push notifications are turned off"
                    return get_success_ok_response(message, self.serializer_class(device).data)
                return get_success_ok_response("No device found for given token", None)
            else:
                return get_error_response("token or active param is missing")
        except Exception as error:
            return get_error_response(str(error))


class GroupViewSet(AppBaseViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user, organisation=request.org)
            return get_create_success_response("Group", serializer.data)
        except Exception as error:
            return get_error_response(str(error))

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.filter(organisation=request.org)
            page = self.paginate_queryset(queryset)
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        except Exception as error:
            return get_error_response(str(error))

    def destroy(self, request, *args, **kwargs):
        try:
            group = self.get_object()
            transfer_to = request.query_params.get("transfer_to")
            if group.organisation == request.org:
                if not group.is_default:
                    if transfer_to:
                        if group.id != int(transfer_to):
                            users = models.User.objects.filter(groups=group)
                            for user in users:
                                user.groups.add(transfer_to)
                            super(GroupViewSet, self).destroy(request, *args, **kwargs)
                            return get_delete_success_response("Profile")
                        return get_error_response("Role can not be transfer to deleted role")
                    return get_error_response("transfer_to missing in params")
                return get_error_response("Default profile can not be deleted")
            return get_error_response("You can not delete other organisation profile")
        except Exception as error:
            return get_error_response(error.args)


class RoleViewSet(AppBaseViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = OrderedDict()
            data.update(request.data)
            data["organisation"] = request.org.pk
            data["created_by"] = request.user.pk
            data["is_deletable"] = True
            parent = data.get("parent")
            if type(parent) == str and "root" in parent:
                root_role = models.Role.objects.filter(organisation=request.org, level=0).first()
                data["parent"] = root_role.pk
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_create_success_response("Role", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.queryset.filter(Q(organisation=None) | Q(organisation=request.org))
            result = []
            for q in queryset:
                if not q.is_child_node():
                    data = recursive_node_to_dict(q)
                    result.append(data)
            if len(result) > 0:
                result[0]["id"] = "root"
            ids = queryset.values_list("id", flat=True)
            final_data = {
                "ids": set(ids),
                "data": result
            }
            return get_list_success_response("Roles", final_data)
        except Exception as error:
            return get_error_response(error.args)

    def update(self, request, *args, **kwargs):
        try:
            data = OrderedDict()
            data.update(request.data)
            data["organisation"] = request.org.pk
            data["created_by"] = request.user.pk
            data["is_deletable"] = True
            parent = data.get("parent")
            if type(parent) == str and "root" in parent:
                root_role = models.Role.objects.filter(organisation=request.org, level=0).first()
                data["parent"] = root_role.pk
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_update_success_response("Role", serializer.data)
        except Exception as error:
            return get_error_response(error.args)

    def destroy(self, request, *args, **kwargs):
        try:
            role = self.get_object()
            transfer_to = request.query_params.get("transfer_to")
            if role.organisation == request.org:
                if not role.is_default:
                    if transfer_to:
                        if transfer_to == "root":
                            transfer_to = models.Role.objects.filter(organisation=request.org, level=0).first().pk
                        if role.id != int(transfer_to):
                            models.Profile.objects.filter(role=role).update(role=transfer_to)
                            super(RoleViewSet, self).destroy(request, *args, **kwargs)
                            return get_delete_success_response("Role")
                        return get_error_response("Role can not be transfer to deleted role")
                    return get_error_response("transfer_to missing in params")
                return get_error_response("Default role can not be deleted")
            return get_error_response("You can not delete other organisation role")
        except Exception as error:
            return get_error_response(error.args)


class BillingDetailViewSet(AppBaseViewSet):
    queryset = models.BillingDetail.objects.all()
    serializer_class = serializers.BillingDetailSerializer

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset().filter(organisation=request.org, user=request.user))
            serializer = self.get_serializer(queryset, many=True)
            return get_list_success_response("Billing details", serializer.data)
        except Exception as error:
            return get_error_response(str(error))

    def create(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            data["organisation"] = request.org.pk
            data["user"] = request.user.pk
            serializer = self.get_serializer(data=data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_update_success_response("Branch Department", serializer.data)
        except Exception as error:
            return get_error_response(str(error))
