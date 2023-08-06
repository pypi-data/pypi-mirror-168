from django.contrib import admin, messages

from . import models


@admin.register(models.Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', ]


@admin.register(models.Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'organisation', 'is_default', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', ]
    actions = ["make_default", "remove_default"]

    @admin.action(description="Make default")
    def make_default(self, request, queryset):
        try:
            queryset.update(is_default=True)
            self.message_user(request, "Selected branches marked as default.",
                              messages.SUCCESS)
        except Exception as error:
            self.message_user(request, str(error),
                              messages.ERROR)

    @admin.action(description="Remove default")
    def remove_default(self, request, queryset):
        try:
            queryset.update(is_default=False)
            self.message_user(request, "Selected branches removed from defaults.",
                              messages.SUCCESS)
        except Exception as error:
            self.message_user(request, str(error),
                              messages.ERROR)


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at', 'updated_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['name', ]


# @admin.register(models.OrganisationSubscription)
# class OrganisationSubscriptionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'organisation', 'subscription', 'cycle', 'purchase_date', 'expire_date']
#     autocomplete_fields = ['organisation', 'subscription']
#     search_fields = ["organisation__name", "subscription__name", "cycle__name"]
