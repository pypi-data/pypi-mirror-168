import datetime
from re import sub

# import razorpay
from django.conf import settings
from django.contrib.auth.models import update_last_login
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
# from fcm_django.models import FCMDevice
from rest_framework_simplejwt.tokens import RefreshToken
from sendgrid import Mail

# from common.models import Notification, CustomFormat
# from payment_gateway.models import PaymentCredential
# from permission.models import DashboardPermission, SettingPermission
# from permission.serializers import CustomImportExportPermissionSerializer, CustomPermissionSerializer, \
#     DashboardPermissionSerializer, SettingPermissionSerializer, CustomBulkActionPermissionSerializer, \
#     CustomEmailPermissionSerializer
from cleverstack_auth.models import CustomGroup as Group, Profile, TOKEN_GENERATOR_CLASS, User, GenerateToken


# def add_permissions(request, group, content_types):
#     email_options = ["send_email", "bulk_email", "delete_email", "merge_email"]
#     bulk_options = ["bulk_delete", "bulk_update",
#                     "change_owner", "bulk_transfer", "convert"]
#     dashboard_permission, created = DashboardPermission.objects.get_or_create(
#         group=group)
#     dashboard_permission.models.set(content_types)
#
#     for opt in ["import", "export"]:
#         import_export_permission, created = ImportExportPermission.objects.get_or_create(
#             group=group,
#             name=opt,
#             is_default=True
#         )
#         import_export_permission.models.set(content_types)
#
#     for opt in email_options:
#         email_permission, created = SendEmailPermission.objects.get_or_create(
#             name=opt, group=group, is_default=True)
#         email_permission.models.set(content_types)
#
#     for opt in bulk_options:
#         bulk_permission, created = BulkActionPermission.objects.get_or_create(
#             name=opt, group=group, is_default=True)
#         bulk_permission.models.set(content_types)
#
#     setting_permission, created = SettingPermission.objects.get_or_create(
#         group=group)
#     setting_permission.organisation = request.org
#     setting_permission.save()
#     setting_permission.models.set(content_types)


# def get_razor_client():
#     if PaymentCredential.objects.filter(organisation=None, is_default=True).exists():
#         payment_method = PaymentCredential.objects.filter(
#             organisation=None, is_default=True).first()
#         client = None
#         if payment_method.name == "razorpay":
#             client = razorpay.Client(
#                 auth=(payment_method.public_key, payment_method.secret_key))
#         return client
#     return None


def get_org_admins(request):
    users = Profile.objects.filter(
        org=request.org).values_list('user', flat=True)
    user_ids = []
    for user in users:
        user_ids.append(user)
    return user_ids


# def generate_complaint_id(request):
#     complaint_id_format = ""
#     complaint_id = None
#     c_i_format = None
#     if CustomFormat.objects.filter(organisation=request.org, model=get_c_type("ticket")).exists():
#         c_i_format = CustomFormat.objects.get(
#             organisation=request.org, model=get_c_type("ticket"))
#     else:
#         c_i_format = CustomFormat.objects.filter(
#             model=get_c_type("ticket"), organisation=None).first()
#     last_ticket = Ticket.objects.filter(organisation=request.org)
#     complaint_id_format = c_i_format.prefix
#     if c_i_format.include_date:
#         complaint_id_format += c_i_format.separator + \
#                                str(datetime.date.today())
#     if c_i_format.include_date_time:
#         complaint_id_format += c_i_format.separator + \
#                                str(datetime.datetime.now())
#     complaint_id_format += c_i_format.separator + \
#                            str(c_i_format.increment_zeros)
#     new_id = None
#     if last_ticket.exists():
#         if c_i_format.separator in last_ticket.latest("created_at").complaint_id:
#             try:
#                 new_id = int(last_ticket.latest("created_at").complaint_id.split(
#                     c_i_format.separator)[-1]) + 1
#             except:
#                 new_id = int(last_ticket.latest("created_at").complaint_id.split(
#                     c_i_format.separator)[-2]) + 1
#             complaint_id_format += str(new_id)
#     else:
#         complaint_id_format += str(1)
#     if not c_i_format.suffix:
#         while Ticket.objects.filter(complaint_id=complaint_id_format).exists():
#             complaint_id_format += str(int(complaint_id_format[-1]) + 1)
#     if c_i_format.suffix:
#         complaint_id_format += c_i_format.separator + str(c_i_format.suffix)
#         while Ticket.objects.filter(complaint_id=complaint_id_format).exists():
#             complaint_id_format += str(int(complaint_id_format[-2]) + 1)
#     return complaint_id_format


# def send_notification(request, title, body, users, ticket, cnt_type):
#     user_devices = FCMDevice.objects.filter(user_id__in=users, active=True)
#     login_user_sms_subject = "Dear {}, Your ticket has been created with the ticket ID {} and subject {} Someone from " \
#                              "our customer service team will review it and respond shortly. Regards, HelpDesk Support" \
#                              " Team. CleverStack".format(request.user.get_full_name, ticket.complaint_id,
#                                                          ticket.subject)
#     for device in user_devices:
#         settings.PUSH_SERVICE.notify_single_device(registration_id=device.registration_id, message_title=title)
#     for user_id in users:
#         if user_id:
#             user = User.objects.get(id=user_id)
#             send_email(user.email, title, body)
#         Notification.objects.create(
#             model=cnt_type,
#             object_id=ticket.id,
#             receiver_id=user_id,
#             sender_id=request.user.id,
#             payload=body, title=title
#         )


def recursive_node_to_dict(_node):
    _data = {
        'id': _node.pk,
        'name': _node.name,
        'is_default': _node.is_default if hasattr(_node, "is_default") else None
    }
    if _node.get_children():
        _data['children'] = [recursive_node_to_dict(
            c) for c in _node.get_children()]
    return _data


def send_email(email, subject, message):
    message = Mail(
        from_email='support@cleverstack.in',
        to_emails=email,
        subject=subject,
        plain_text_content=message)
    client = getattr(settings, "SEND_GRID_CLIENT")
    client.send(message)


def send_otp_via_email(user, request):
    key = TOKEN_GENERATOR_CLASS.generate_token()
    while GenerateToken.objects.filter(key=key).exists():
        key = TOKEN_GENERATOR_CLASS.generate_token()
    ip, user_agent = get_ip_and_user_agent(request)
    token = GenerateToken.objects.create(
        user=user, ip_address=ip, user_agent=user_agent, key=key)
    messages = 'Thank you for creating a CleverStack account. \n {} is your otp to verify/activate your account. ' \
               '\n Team CleverStack'.format(token.key)
    subject = "CleverStack Account Verification"
    message = Mail(
        from_email='support@cleverstack.in',
        to_emails=user.email,
        subject=subject,
        plain_text_content=messages)
    client = getattr(settings, "SEND_GRID_CLIENT")
    client.send(message)


def get_user_group_ids(user):
    group_ids = user.groups.values_list("id", flat=True)
    return group_ids


def get_login_info(user, request):
    token = RefreshToken.for_user(user)
    user_groups = user.groups.values_list("id", flat=True)
    update_last_login(None, user)
    # org_subscriptions = OrganisationSubscription.objects.filter(organisation=user.user_profile.org, is_active=True)
    is_trial = False
    is_subscribed = False
    users_in_subscription = 0
    subscription_id = None
    cycle_id = None
    expired_at = None
    # if org_subscriptions.filter(subscription__is_trial=True).exists():
    #     is_trial = True
    #     expired_at = org_subscriptions.filter(subscription__is_trial=True).first().expire_date
    # elif org_subscriptions.filter(subscription__is_trial=False).exists():
    #     subscription = org_subscriptions.filter(subscription__is_trial=False).first()
    #     subscription_id = subscription.subscription_id
    #     cycle_id = subscription.cycle_id
    #     is_subscribed = True
    #     users_in_subscription = subscription.users
    #     expired_at = subscription.expire_date
    fcm_device = None
    device_token = request.data.get("device_token")
    # if device_token:
    #     fcm_device, _ = FCMDevice.objects.get_or_create(
    #         user_id=user.id, registration_id=device_token)
    groups = []
    for group in user.groups.all():
        groups.append({"id": group.id, "name": group.name})
    data = {
        'refresh': str(token),
        'access': str(token.access_token),
        'email': user.email,
        'user_id': user.id,
        'username': user.username,
        'profiles': groups,
        'is_active': user.is_active,
        'is_verified': user.is_verified,
        'image': user.user_profile.image.url if user.user_profile.image else None,
        'last_login': user.last_login,
        'role': user.user_profile.role.name if user.user_profile.role else None,
        'org_name': user.user_profile.org.name,
        'org_id': user.user_profile.org.id,
        'is_admin': user.is_owner,
        'is_staff': user.is_org_staff,
        'is_customer': user.is_customer,
        'is_subscribed': is_subscribed,
        'is_trial': is_trial,
        'expired_at': expired_at,
        'users_limit': users_in_subscription,
        'subscription_id': subscription_id,
        'cycle_id': cycle_id,
        # 'push_notification_status': fcm_device.active if fcm_device else None,
        # 'crud_permissions': get_crud_permissions(user_groups, request),
        # 'email_permissions': get_email_permissions(user_groups),
        # 'import_export_permissions': get_import_export_permissions(user_groups),
        # 'bulk_action_permissions': get_bulk_action_permissions(user_groups),
        # 'filter_permissions': get_filter_permissions(user_groups),
        # 'setting_permissions': get_setting_permissions(user_groups),
        # 'dashboard_permissions': get_dashboard_permissions(user_groups)
    }
    return data


def fields_lookups(model):
    lookups = {}

    fields = [x.name for x in model._meta.fields]
    for field in fields:
        lookups[field] = [*model._meta.get_field(
            field).get_lookups().keys()]
    return lookups


# error message for small models
def get_short_error_message(error):
    message = ""
    for k, v in error.args[0].items():
        try:
            message += error.args[0][k]
        except TypeError as e:
            message += error.args[0][k][0]
    return message


def get_c_type(model):
    return ContentType.objects.get(model__iexact=model)


def get_ip_and_user_agent(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    user_agent = request.META.get('HTTP_USER_AGENT')
    return ip, user_agent


def jwt_payload_handler(user):
    """Custom payload handler
    Token encrypts the dictionary returned by this function, and can be
    decoded by rest_framework_jwt.utils.jwt_decode_handler
    """
    return {
        "id": user.pk,
        "email": user.email,
        "company": user.company.id,
        "role": user.role,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "is_staff": user.is_staff,
        # "date_joined"
    }

# def get_crud_permissions(group_ids, request):
#     group = Group.objects.filter(id__in=group_ids).order_by("permissions__content_type__model").distinct(
#         "permissions__content_type__model").first()
#     permissions = None
#     model_list = [
#         'lead', 'contact', 'account', 'ticket', "note", "task", 'meeting',
#         "attachment", "notification", "status", "language", "channel", "priority",
#         "classification", "resolution", "listingpreference", "pinningreference", "customfield",
#         "customformat", "source", "tag", "comment", "reply", "priority", "department",
#         "classification", "estimate", "saleorder", "deliverychallan", "invoice", "history",
#         "user", "branch", "role", "customgroup", "group"
#     ]
#     if group:
#         permissions = group.permissions.filter(
#             content_type__model__in=model_list
#         ).order_by("content_type").distinct("content_type")
#         serializer = CustomPermissionSerializer(
#             permissions, many=True, context={'group': group})
#         return serializer.data
#     permissions = request.user.user_permissions.filter(
#         content_type__model__in=model_list
#     ).order_by("content_type").distinct("content_type")
#     serializer = CustomPermissionSerializer(
#         permissions, many=True, context={'user': request.user})
#     return serializer.data


# def get_filter_permissions(group_ids):
#     filter_permissions = FilterPermission.objects.filter(
#         group_id__in=group_ids)
#     serializer = FilterPermissionSerializer(filter_permissions, many=True)
#     return serializer.data


# def get_dashboard_permissions(group_ids):
#     permission = DashboardPermission.objects.filter(
#         group_id__in=group_ids).first()
#     serializer = DashboardPermissionSerializer(permission)
#     return serializer.data


# def get_setting_permissions(group_ids):
#     setting_permissions = SettingPermission.objects.filter(
#         group_id__in=group_ids)
#     serializer = SettingPermissionSerializer(setting_permissions, many=True)
#     return serializer.data


# def get_bulk_action_permissions(group_ids):
#     group = Group.objects.filter(
#         id__in=group_ids
#     ).order_by("permissions__codename").distinct("permissions__codename").first()
#     if group:
#         perms = group.bulk_action_permission.all()
#         serializer = CustomBulkActionPermissionSerializer(perms, many=True)
#         return serializer.data
#     return []


# def get_email_permissions(group_ids):
#     group = Group.objects.filter(
#         id__in=group_ids
#     ).order_by("permissions__codename").distinct("permissions__codename").first()
#     if group:
#         perms = group.email_permission.all()
#         serializer = CustomEmailPermissionSerializer(perms, many=True)
#         return serializer.data
#     return []


# def get_import_export_permissions(group_ids):
#     group = Group.objects.filter(
#         id__in=group_ids
#     ).order_by("permissions__codename").distinct("permissions__codename").first()
#     if group:
#         perms = group.import_export_permission.all()
#         serializer = CustomImportExportPermissionSerializer(perms, many=True)
#         return serializer.data
#     return []
