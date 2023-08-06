from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from django.dispatch import receiver

from organisation.models import Organisation
from permission.models import ImportExportPermission, SendEmailPermission, BulkActionPermission, SettingPermission, \
    DashboardPermission, AdminPermission
from user.models import CustomGroup


@receiver(post_save, sender=Organisation)
def post_org_data(sender, instance, *args, **kwargs):
    """
    This is Post Save Organisation signal.
    Here, default permissions and groups are being created for a particular organisation
    """

    email_options = ["send_email", "bulk_email", "delete_email", "merge_email"]
    bulk_options = ["bulk_delete", "bulk_update", "change_owner", "bulk_transfer", "convert"]
    default_models = ContentType.objects.filter(model__in=["lead", "ticket", "contact", "account"])
    default_permissions = Permission.objects.filter(content_type__model__in=["note", "attachment"]).values_list("id",
                                                                                                                flat=True)

    # Default permissions for Administrator group
    admin, _ = CustomGroup.objects.get_or_create(organisation=instance, name="Administrator", is_default=True)
    perms = Permission.objects.values_list("id", flat=True)
    admin.permissions.set(perms)
    admin.default_permissions.set(default_permissions)
    import_export_perms = ImportExportPermission.objects.create(name="import", group=admin, is_default=True)
    import_export_perms.models.set(default_models)
    import_export_perms = ImportExportPermission.objects.create(name="export", group=admin, is_default=True)
    import_export_perms.models.set(default_models)
    for opt in email_options:
        email_perms = SendEmailPermission.objects.create(name=opt, group=admin, is_default=True)
        email_perms.models.set(default_models)
    for opt in bulk_options:
        bulk_perms = BulkActionPermission.objects.create(name=opt, group=admin, is_default=True)
        bulk_perms.models.set(default_models)
    setting_perms = SettingPermission.objects.create(organisation=instance, group=admin, is_default=True)
    setting_perms.models.set(default_models)
    dashboard_perms = DashboardPermission.objects.create(organisation=instance, group=admin, is_default=True)
    dashboard_perms.models.set(default_models)
    admin_perms = AdminPermission.objects.create(group=admin, compliance_settings=False, module_customization=False,
                                                 is_default=True)
    admin_perms.user_management.set(ContentType.objects.filter(model__in=["user", "group", "role"]))

    # Default permissions for Standard group
    standard, _ = CustomGroup.objects.get_or_create(organisation=instance, name="Standard", is_default=True)
    models = ["ticket", "product", "user", "profile", "comment", "reply", "notification", "status", "tag", "source",
              "language", "channel", "department", "classification", "timeentry", "timeentrytype", "history",
              "attachment", "task", "meeting"]
    perms = Permission.objects.filter(content_type__model__in=models).values_list("id", flat=True)
    standard.permissions.set(perms)
    standard.default_permissions.set(default_permissions)
    import_export_perms = ImportExportPermission.objects.create(name="import", group=standard, is_default=True)
    import_export_perms.models.set(default_models)
    import_export_perms = ImportExportPermission.objects.create(name="export", group=standard, is_default=True)
    import_export_perms.models.set(default_models)
    for opt in email_options:
        email_perms = SendEmailPermission.objects.create(name=opt, group=standard, is_default=True)
        email_perms.models.set(default_models)
    for opt in bulk_options:
        bulk_perms = BulkActionPermission.objects.create(name=opt, group=standard, is_default=True)
        bulk_perms.models.set(default_models)
    setting_perms = SettingPermission.objects.create(organisation=instance, group=standard, is_default=True)
    setting_perms.models.set(default_models)
    dashboard_perms = DashboardPermission.objects.create(organisation=instance, group=standard, is_default=True)
    dashboard_perms.models.set(default_models)
    admin_perms = AdminPermission.objects.create(group=standard, compliance_settings=False, module_customization=False,
                                                 is_default=True)
    admin_perms.user_management.set([])
