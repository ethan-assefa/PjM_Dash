# accounts/migrations/0003_create_default_groups.py

from django.db import migrations

# Create three default groups with the appropriate settings
def create_default_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Important: use the same DB alias as the migration is applying to
    db_alias = schema_editor.connection.alias

    # 1) Admin group: all permissions
    admin_group, _ = Group.objects.using(db_alias).get_or_create(name='Admin')
    all_perms = Permission.objects.using(db_alias).all()
    admin_group.permissions.set(all_perms)

    # 2) Lead group: only 'add_' / 'change_'
    lead_group, _ = Group.objects.using(db_alias).get_or_create(name='Lead')
    lead_perms = Permission.objects.using(db_alias).filter(
        codename__startswith=('add_', 'change_')
    )
    lead_group.permissions.set(lead_perms)

    # 3) User group: minimal perms
    user_group, _ = Group.objects.using(db_alias).get_or_create(name='User')
    user_group.permissions.clear()

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),  # or your current auth migration
        ('accounts', '0002_extra_constraints'),
    ]

    operations = [
        migrations.RunPython(create_default_groups),
    ]
