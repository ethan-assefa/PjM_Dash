from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
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

# For models that don’t need special customization, do a simple register:
admin.site.register(Auditlogs)
admin.site.register(Collaborators)
admin.site.register(Deliverables)
admin.site.register(ProjectCollaborators)
admin.site.register(Projects)
admin.site.register(TaskDeliverables)
admin.site.register(Tasks)
admin.site.register(Updates)
