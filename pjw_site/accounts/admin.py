from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser,
    Auditlogs,
    Collaborators,
    Deliverables,
    ProjectCollaborators,
    Projects,
    TaskDeliverables,
    Tasks,
    Updates,
)

# Register your models here.

# Register CustomUser with Django’s built-in UserAdmin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # To get default UserAdmin’s fieldsets plus the custom user_role:
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_role',)}),
    )

# For models that don’t need special customization, do a simple register:
admin.site.register(Auditlogs)
admin.site.register(Collaborators)
admin.site.register(Deliverables)
admin.site.register(ProjectCollaborators)
admin.site.register(Projects)
admin.site.register(TaskDeliverables)
admin.site.register(Tasks)
admin.site.register(Updates)
