from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from mptt.models import MPTTModel
from phonenumber_field.modelfields import PhoneNumberField

from cleverstack_auth.base.models import BaseModel


# from subscription.models import Subscription, SubscriptionCycle


class Organisation(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_organisation", "Access"),
            ("detail_organisation", "View"),
            ("view_organisation", "List"),
            ("change_organisation", "Edit"),
            ("delete_organisation", "Delete"),
            ("add_organisation", "Create"),
        )


class Branch(MPTTModel, BaseModel):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="org_branches")
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255, null=True, blank=True)
    manager = models.ForeignKey("cleverstack_auth.User", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="branch_managers")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_branch", "Access"),
            ("detail_branch", "View"),
            ("view_branch", "List"),
            ("change_branch", "Edit"),
            ("delete_branch", "Delete"),
            ("add_branch", "Create"),
        )

    def __str__(self):
        return "{} : {}".format(self.id, self.name)


class Department(MPTTModel, BaseModel):
    organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, related_name="branch_departments")
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="departments")
    name = models.CharField(max_length=200)
    manager = models.ForeignKey("cleverstack_auth.User", on_delete=models.SET_NULL, null=True, blank=True,
                                related_name="department_manager")
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        default_permissions = []
        permissions = (
            ("access_department", "Access"),
            ("detail_department", "View"),
            ("view_department", "List"),
            ("change_department", "Edit"),
            ("delete_department", "Delete"),
            ("add_department", "Create"),
        )

    def __str__(self):
        return "{} : {}".format(self.id, self.name)

# class OrganisationSubscription(BaseModel):
#     organisation = models.ForeignKey(Organisation, on_delete=models.CASCADE, blank=True, null=True)
#     # subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, blank=True, null=True,
#     #                                  related_name='organisation_subscription')
#     cycle = models.ForeignKey("subscription.SubscriptionCycle", on_delete=models.CASCADE, blank=True, null=True,
#                               related_name='organisation_cycle')
#     addons = models.ManyToManyField("subscription.Addon", blank=True, related_name="org_addons")
#     users = models.PositiveIntegerField(default=0)
#     amount = models.PositiveIntegerField()
#     is_active = models.BooleanField(default=True)
#     purchase_date = models.DateTimeField(blank=True, null=True)
#     expire_date = models.DateTimeField(blank=True, null=True)
#
#     def __str__(self):
#         return str(self.id)
#
#     class Meta:
#         ordering = ["-created_at"]
#         default_permissions = []
#         permissions = (
#             ("access_organisationsubscription", "Access"),
#             ("detail_organisationsubscription", "View"),
#             ("view_organisationsubscription", "List"),
#             ("change_organisationsubscription", "Edit"),
#             ("delete_organisationsubscription", "Delete"),
#             ("add_organisationsubscription", "Create"),
#         )


# @receiver(pre_save, sender=OrganisationSubscription)
# def pre_save_expire_date_receiver(sender, instance, *args, **kwargs):
#     if instance.subscription:
#         instance.expire_date = instance.purchase_date + timezone.timedelta(instance.cycle.interval)
