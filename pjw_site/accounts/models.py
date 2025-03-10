from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# Manages user creation so that any superuser has user_role automatically set to "Admin"
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('user_role', 'Admin')
        return super().create_superuser(username, email, password, **extra_fields)


# -------------------------------------------------------------------------------------
# CUSTOM USER MODEL (replaces "Users" table)
# -------------------------------------------------------------------------------------
class CustomUser(AbstractUser):
    id = models.AutoField(primary_key=True)

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Lead',  'Lead'),
        ('User',  'User'),
    )
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')

    objects = CustomUserManager()

    class Meta:
        db_table = 'Users'
        managed = True  # Let Django create/alter this table


# -------------------------------------------------------------------------------------
# AUDIT LOGS
# (Still referencing "Users" by user_id = 'id' column, but we keep managed=False if
#  you have special constraints or prefer to keep it out of migrations.)
# -------------------------------------------------------------------------------------
class Auditlogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    # DO_NOTHING means no cascade or set-null; it will raise errors if user is deleted
    user = models.ForeignKey('CustomUser', on_delete=models.DO_NOTHING, db_column='id')
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
        managed = True  # Let Django create the table from scratch if desired


# -------------------------------------------------------------------------------------
# PROJECTS
# (created_by -> user, no cascade, so do_noting or protect; we'll do DO_NOTHING)
# -------------------------------------------------------------------------------------
class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100)
    proj_describe = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    proj_status = models.CharField(max_length=15)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,   # "NO ACTION" style
        db_column='created_by'
    )
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Projects'
        managed = True


# -------------------------------------------------------------------------------------
# DELIVERABLES
# (project -> on_delete=models.CASCADE, created_by -> on_delete=DO_NOTHING)
# -------------------------------------------------------------------------------------
class Deliverables(models.Model):
    deliverable_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE,  # per your SQL "ON DELETE CASCADE"
    )
    deliverable_name = models.CharField(max_length=100)
    deliverable_describe = models.TextField(blank=True, null=True)
    deliverable_status = models.CharField(max_length=15)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        db_column='created_by'
    )

    class Meta:
        db_table = 'Deliverables'
        managed = True


# -------------------------------------------------------------------------------------
# PROJECT-COLLABORATORS M2M TABLE
# (project -> CASCADE, collaborator -> CASCADE, plus unique_together)
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
# (project -> CASCADE, assigned_to -> SET_NULL, created_by -> DO_NOTHING)
# -------------------------------------------------------------------------------------
class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    task_name = models.CharField(max_length=100)
    assigned_to = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,   # "ON DELETE SET NULL"
        db_column='assigned_to',
        blank=True, null=True
    )
    task_status = models.CharField(max_length=15)
    task_priority = models.CharField(max_length=10)
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        db_column='created_by',
        related_name='tasks_created_by_set'
    )

    class Meta:
        db_table = 'Tasks'
        managed = True


# -------------------------------------------------------------------------------------
# TASK-DELIVERABLES M2M TABLE
# (unique_together on (task, deliverable), plus partial cascade?)
# We'll do on_delete=CASCADE for deliverable; on_delete=DO_NOTHING for task, etc.
# You can tweak if needed.
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
# (project -> CASCADE, created_by -> DO_NOTHING)
# -------------------------------------------------------------------------------------
class Updates(models.Model):
    update_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        Projects,
        on_delete=models.CASCADE
    )
    update_text = models.TextField()
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.DO_NOTHING,
        db_column='created_by'
    )
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'Updates'
        managed = True
