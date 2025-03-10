# accounts/models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Use default user table

# -------------------------------------------------------------------------------------
# AUDITLOGS
# -------------------------------------------------------------------------------------
class Auditlogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column='id'
    )
    act = models.TextField()
    audit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'AuditLogs'
        managed = True


# -------------------------------------------------------------------------------------
# COLLABORATORS
# -------------------------------------------------------------------------------------
class Collaborators(models.Model):
    collaborator_id = models.AutoField(primary_key=True)
    collab_name = models.CharField(max_length=100)
    collab_describe = models.TextField(blank=True, null=True)
    is_funder = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Collaborators'
        managed = True


# -------------------------------------------------------------------------------------
# PROJECTS
# -------------------------------------------------------------------------------------
class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    proj_describe = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    proj_status = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column='created_by'
    )
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Projects'
        managed = True


# -------------------------------------------------------------------------------------
# DELIVERABLES
# -------------------------------------------------------------------------------------
class Deliverables(models.Model):
    deliverable_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    deliverable_name = models.CharField(max_length=100)
    deliverable_describe = models.TextField(blank=True, null=True)
    deliverable_status = models.CharField(max_length=15)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column='created_by'
    )

    class Meta:
        db_table = 'Deliverables'
        managed = True


# -------------------------------------------------------------------------------------
# PROJECT-COLLABORATORS M2M
# -------------------------------------------------------------------------------------
class ProjectCollaborators(models.Model):
    projcollab_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    collaborator = models.ForeignKey(
        Collaborators,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'Project_Collaborators'
        managed = True
        unique_together = (('project', 'collaborator'),)


# -------------------------------------------------------------------------------------
# TASKS
# -------------------------------------------------------------------------------------
class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    task_name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        db_column='assigned_to',
        blank=True, null=True
    )
    task_status = models.CharField(max_length=15)
    task_priority = models.CharField(max_length=10)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column='created_by',
        related_name='tasks_created_by_set'
    )

    class Meta:
        db_table = 'Tasks'
        managed = True


# -------------------------------------------------------------------------------------
# TASK-DELIVERABLES M2M
# -------------------------------------------------------------------------------------
class TaskDeliverables(models.Model):
    taskdeliv_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        Tasks,
        on_delete=models.DO_NOTHING
    )
    deliverable = models.ForeignKey(
        Deliverables,
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'Task_Deliverables'
        managed = True
        unique_together = (('task', 'deliverable'),)


# -------------------------------------------------------------------------------------
# UPDATES
# -------------------------------------------------------------------------------------
class Updates(models.Model):
    update_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    update_text = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        db_column='created_by'
    )
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Updates'
        managed = True
