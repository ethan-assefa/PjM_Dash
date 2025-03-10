# Generated by Django 5.0.8 on 2025-03-10 07:19

import accounts.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auditlogs',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('act', models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')),
                ('audit_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'AuditLogs',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Collaborators',
            fields=[
                ('collaborator_id', models.AutoField(primary_key=True, serialize=False)),
                ('collab_name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
                ('collab_describe', models.TextField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', null=True)),
                ('is_funder', models.BooleanField()),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Collaborators',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Deliverables',
            fields=[
                ('deliverable_id', models.AutoField(primary_key=True, serialize=False)),
                ('deliverable_name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
                ('deliverable_describe', models.TextField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', null=True)),
                ('deliverable_status', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=15)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Deliverables',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectCollaborators',
            fields=[
                ('projcollab_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Project_Collaborators',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('project_id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
                ('proj_describe', models.TextField(blank=True, db_collation='SQL_Latin1_General_CP1_CI_AS', null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('proj_status', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=15)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Projects',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TaskDeliverables',
            fields=[
                ('taskdeliv_id', models.AutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Task_Deliverables',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Tasks',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False)),
                ('task_name', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=100)),
                ('task_status', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=15)),
                ('task_priority', models.CharField(db_collation='SQL_Latin1_General_CP1_CI_AS', max_length=10)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Tasks',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Updates',
            fields=[
                ('update_id', models.AutoField(primary_key=True, serialize=False)),
                ('update_text', models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'Updates',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_role', models.CharField(choices=[('Admin', 'Admin'), ('Lead', 'Lead'), ('User', 'User')], default='User', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'Users',
                'managed': True,
            },
            managers=[
                ('objects', accounts.models.CustomUserManager()),
            ],
        ),
    ]
