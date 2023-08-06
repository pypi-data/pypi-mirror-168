import re

from rest_framework import serializers

# from subscription.serializers import SubscriptionSerializer
from cleverstack_auth.models import Profile, User
from . import models


class CheckOrganisationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True, required=False)
    email = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['name', 'email', 'mobile']

    def validate_name(self, name):
        if name:
            if bool(re.search(r"[~\!_.@#\$%\^&\*\ \(\)\+{}\":;'/\[\]]", name)):
                raise serializers.ValidationError(
                    "organization name should not contain any special characters")
            if models.Organisation.objects.filter(name=name.lower()).exists():
                raise serializers.ValidationError("Organization already exists with this name")
            return name

    def validate_email(self, email):
        if email:
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError("Email already exists")
            return email

    def validate_mobile(self, mobile):
        if mobile:
            if User.objects.filter(mobile=mobile).exists():
                raise serializers.ValidationError("Mobile number already exists")
            return mobile


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "mobile", "first_name", "last_name", "password")

    def validate(self, attrs):
        password = attrs['password']
        org_name = self.initial_data.get('name')
        email = attrs['email']
        mobile = attrs['mobile']
        if password:
            if len(password) < 4:
                raise serializers.ValidationError("Password must be at least 4 characters long!")
        if org_name:
            if bool(re.search(r"[~\!_.@#\$%\^&\*\ \(\)\+{}\":;'/\[\]]", org_name)):
                raise serializers.ValidationError(
                    "organization name should not contain any special characters")
            if models.Organisation.objects.filter(name=org_name.lower()).exists():
                raise serializers.ValidationError("Organization already exists with this name")
        if email:
            if User.objects.filter(email__iexact=email).exists():
                raise serializers.ValidationError("Email already exists")
        if mobile:
            if User.objects.filter(mobile=mobile).exists():
                raise serializers.ValidationError("Mobile number already exists")
        super(OrganizationSerializer, self).validate(attrs)
        return attrs


# class OrganisationSubscriptionSerializer(serializers.ModelSerializer):
#     subscription = SubscriptionSerializer(many=False)
#
#     class Meta:
#         model = models.OrganisationSubscription
#         fields = ["id", "organisation", "subscription", "purchase_date", "expire_date"]


class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = ["id", "name", "organisation", "location", "parent", "description", "created_at", "updated_at",
                  "manager", "is_default"]

    def __init__(self, *args, **kwargs):
        self.org = kwargs.pop("org", None)
        super(BranchSerializer, self).__init__(*args, **kwargs)

    def validate_name(self, name):
        if self.instance:
            if self.instance.name != name:
                if models.Branch.objects.filter(name=name, organisation=self.org).exists():
                    raise serializers.ValidationError("Branch already exists with this name")
                return name
            return name
        else:
            if models.Branch.objects.filter(name=name, organisation=self.org).exists():
                raise serializers.ValidationError("Branch already exists with this name")
            else:
                return name

    def to_representation(self, instance):
        data = super(BranchSerializer, self).to_representation(instance)
        if instance.organisation:
            data["organisation"] = instance.organisation.name
        if instance.manager:
            data["manager"] = {"id": instance.manager.pk, "email": instance.manager.email}
        if instance.organisation:
            data["organisation"] = instance.organisation.name
        if instance.parent:
            data["parent"] = {"id": instance.parent.pk, "name": instance.parent.name}
        users = Profile.objects.filter(branch=instance).values_list("user", flat=True)
        org_users = User.objects.filter(id__in=users)
        users = []
        for user in org_users:
            users.append({"id": user.pk, "email": user.email})
        data["users"] = users
        return data


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Department
        fields = ("id", "name", "organisation", "branch", "manager")
    
    def validate(self, attrs):
        branch = attrs.get("branch")
        name = attrs.get("name")
        if self.instance:
            if name != self.instance.name:
                if models.Department.objects.filter(branch=branch, name=name).exists():
                    raise serializers.ValidationError({"name": "Department already exists with this name in this branch"})
        else:
            if models.Department.objects.filter(branch=branch, name=name).exists():
                raise serializers.ValidationError({"name":"Department already exists with this name in this branch"})
        return attrs


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["manager"] = {"id":instance.manager.id, "name": instance.manager.email} if instance.manager else None
        data["organisation"] = instance.organisation.name if instance.organisation else None
        data["branch"] = {"id": instance.branch.id, "name": instance.branch.name} if instance.branch else None
        return data
