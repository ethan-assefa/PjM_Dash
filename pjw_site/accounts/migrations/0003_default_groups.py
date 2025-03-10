# accounts/migrations/0003_create_default_groups.py

from django.db import migrations

# Create three default groups with the appropriate settings
def create_default_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # 1) Admin group: all permissions
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    all_perms = Permission.objects.all()
    admin_group.permissions.set(all_perms)

    # 2) Lead group: only 'add_' and 'change_' perms, for example
    lead_group, _ = Group.objects.get_or_create(name='Lead')
    lead_perms = Permission.objects.filter(
        codename__startswith=('add_', 'change_')
    )
    lead_group.permissions.set(lead_perms)

    # 3) User group: minimal perms
    user_group, _ = Group.objects.get_or_create(name='User')
    user_group.permissions.clear()  # or add some minimal perms


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_extra_constraints'),
        ('auth', '0012_alter_user_first_name_max_length'),  # or your current auth migration
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]
