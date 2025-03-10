# This is an auto-generated Django model module.

# E: Allows us to map our relational database for Django and have it understand the 
# relationships between different datapoints

# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Manages user creation so that any superuser has user role automatically set to admin
class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        # Force user_role to "Admin" (or any non-null default you want).
        extra_fields.setdefault('user_role', 'Admin')
        return super().create_superuser(username, email, password, **extra_fields)

# Creates custom user class that builds off default django user class (adds user role)
class CustomUser(AbstractUser):
    '''
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    password = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(unique=True, max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    last_login = models.DateTimeField(blank=True, null=True)
    '''
    id = models.AutoField(primary_key=True)

    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Lead', 'Lead'),
        ('User', 'User'),
    )
    user_role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='User')

    # Automates admin setting for user_role when user is superuser
    objects = CustomUserManager()

    class Meta:
        db_table = 'Users'    # Tells Django to use the existing 'Users' table
        managed = True       # Allow Django to create/alter this table via migrations (for full admin/user functionality)

#######################################################################################

# Sets model for audit table of relational DB
class Auditlogs(models.Model):
    log_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='id')
    act = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    audit_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'AuditLogs'

#######################################################################################

# Sets model for collaborators table of relational DB
class Collaborators(models.Model):
    collaborator_id = models.AutoField(primary_key=True)
    collab_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    collab_describe = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    is_funder = models.BooleanField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Collaborators'

#######################################################################################

# Sets model for deliverables table of relational DB
class Deliverables(models.Model):
    deliverable_id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    deliverable_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    deliverable_describe = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    deliverable_status = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='created_by')

    class Meta:
        managed = False
        db_table = 'Deliverables'

#######################################################################################

# Sets model for project-collaborators junction table of relational DB
class ProjectCollaborators(models.Model):
    projcollab_id = models.AutoField(primary_key=True)
    project = models.ForeignKey('Projects', models.DO_NOTHING)
    collaborator = models.ForeignKey(Collaborators, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Project_Collaborators'
        unique_together = (('project', 'collaborator'),)

#######################################################################################

# Sets model for project table of relational DB
class Projects(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    proj_describe = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    proj_status = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_by = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='created_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Projects'

#######################################################################################

# Sets model for task-deliverables junction table of relational DB
class TaskDeliverables(models.Model):
    taskdeliv_id = models.AutoField(primary_key=True)
    task = models.ForeignKey('Tasks', models.DO_NOTHING)
    deliverable = models.ForeignKey(Deliverables, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Task_Deliverables'
        unique_together = (('task', 'deliverable'),)

#######################################################################################

# Sets model for tasks table of relational DB
class Tasks(models.Model):
    task_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, models.DO_NOTHING)
    task_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    assigned_to = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='assigned_to', blank=True, null=True)
    task_status = models.CharField(max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS')
    task_priority = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS')
    due_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='created_by', related_name='tasks_created_by_set')

    class Meta:
        managed = False
        db_table = 'Tasks'

#######################################################################################

# Sets model for updates table of relational DB
class Updates(models.Model):
    update_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Projects, models.DO_NOTHING)
    update_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_by = models.ForeignKey('CustomUser', models.DO_NOTHING, db_column='created_by')
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Updates'
