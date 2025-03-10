# accounts/migrations/0002_extra_constraints.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        # 1) Add a check constraint for Projects.proj_status
        migrations.RunSQL(
            """
            ALTER TABLE [dbo].[Projects]
            ADD CONSTRAINT [CK_Projects_proj_status]
            CHECK (proj_status IN ('Not Started', 'In Progress', 'Completed', 'On Hold'));
            """,
            reverse_sql="""
            ALTER TABLE [dbo].[Projects]
            DROP CONSTRAINT [CK_Projects_proj_status];
            """
        ),

        # 2) Add a check constraint for Deliverables.deliverable_status
        migrations.RunSQL(
            """
            ALTER TABLE [dbo].[Deliverables]
            ADD CONSTRAINT [CK_Deliverables_deliverable_status]
            CHECK (deliverable_status IN ('Not Started', 'In Progress', 'Completed', 'On Hold'));
            """,
            reverse_sql="""
            ALTER TABLE [dbo].[Deliverables]
            DROP CONSTRAINT [CK_Deliverables_deliverable_status];
            """
        ),

        # 3) Add a check constraint for Tasks.task_status
        migrations.RunSQL(
            """
            ALTER TABLE [dbo].[Tasks]
            ADD CONSTRAINT [CK_Tasks_task_status]
            CHECK (task_status IN ('Not Started', 'In Progress', 'Completed'));
            """,
            reverse_sql="""
            ALTER TABLE [dbo].[Tasks]
            DROP CONSTRAINT [CK_Tasks_task_status];
            """
        ),

        # 4) Add a check constraint for Tasks.task_priority
        migrations.RunSQL(
            """
            ALTER TABLE [dbo].[Tasks]
            ADD CONSTRAINT [CK_Tasks_task_priority]
            CHECK (task_priority IN ('Low', 'Medium', 'High'));
            """,
            reverse_sql="""
            ALTER TABLE [dbo].[Tasks]
            DROP CONSTRAINT [CK_Tasks_task_priority];
            """
        ),

        # 5) CREATE TRIGGER before_user_delete referencing the Admin group
        migrations.RunSQL(
            """
            CREATE TRIGGER [before_user_delete]
            ON [dbo].[auth_user]
            INSTEAD OF DELETE
            AS
            BEGIN
                SET NOCOUNT ON;

                -- Get the Admin group id from auth_group
                DECLARE @admin_group_id INT;
                SELECT @admin_group_id = [id]
                FROM [dbo].[auth_group]
                WHERE [name] = 'Admin';

                -- If there's no group named 'Admin', we can't do fallback
                IF @admin_group_id IS NULL
                BEGIN
                    RAISERROR ('Cannot delete user: No "Admin" group found for fallback assignment.', 16, 1);
                    ROLLBACK TRANSACTION;
                    RETURN;
                END;

                -- Find any user in the Admin group to reassign ownership
                DECLARE @fallback_admin INT;
                SELECT TOP 1 @fallback_admin = [id]
                FROM [dbo].[auth_user]
                WHERE [id] IN (
                    SELECT user_id
                    FROM [dbo].[Users_groups]
                    WHERE group_id = @admin_group_id
                );

                IF @fallback_admin IS NULL
                BEGIN
                    RAISERROR ('Cannot delete user: No user in "Admin" group available for fallback assignment.', 16, 1);
                    ROLLBACK TRANSACTION;
                    RETURN;
                END;

                -- Reassign created_by fields from the deleted user to the fallback admin
                UPDATE [dbo].[Projects]
                SET created_by = @fallback_admin
                WHERE created_by IN (SELECT [id] FROM DELETED);

                UPDATE [dbo].[Tasks]
                SET created_by = @fallback_admin
                WHERE created_by IN (SELECT [id] FROM DELETED);

                UPDATE [dbo].[Deliverables]
                SET created_by = @fallback_admin
                WHERE created_by IN (SELECT [id] FROM DELETED);

                UPDATE [dbo].[Updates]
                SET created_by = @fallback_admin
                WHERE created_by IN (SELECT [id] FROM DELETED);

                DELETE FROM [dbo].[auth_user]
                WHERE [id] IN (SELECT [id] FROM DELETED);
            END;
            """,
            reverse_sql="""
            DROP TRIGGER [before_user_delete];
            """
        ),
    ]
