# accounts/migrations/0002_extra_constraints.py

from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),  # or whatever your initial migration is named
    ]

    operations = [
        # 1) Add a check constraint for user_role in Users
        migrations.RunSQL(
            """
            ALTER TABLE [dbo].[Users]
            ADD CONSTRAINT [CK_Users_user_role]
            CHECK (user_role IN ('Admin', 'Lead', 'User'));
            """,
            reverse_sql="""
            ALTER TABLE [dbo].[Users]
            DROP CONSTRAINT [CK_Users_user_role];
            """
        ),

        # 2) Add a check constraint for Projects.proj_status
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

        # 3) Add a check constraint for Deliverables.deliverable_status
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

        # 4) Add a check constraint for Tasks.task_status
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

        # 5) Add a check constraint for Tasks.task_priority
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

        # 6) CREATE TRIGGER before_user_delete on [dbo].[Users]
        migrations.RunSQL(
            """
            CREATE TRIGGER [before_user_delete]
            ON [dbo].[Users]
            INSTEAD OF DELETE
            AS
            BEGIN
                SET NOCOUNT ON;
                DECLARE @fallback_admin INT;

                -- Find an Admin user to take over ownership
                SELECT TOP 1 @fallback_admin = [id]
                FROM [dbo].[Users]
                WHERE user_role = 'Admin';

                -- If no Admin exists, prevent deletion
                IF @fallback_admin IS NULL
                BEGIN
                    RAISERROR ('Cannot delete user: No admin available for reassignment.', 16, 1);
                    ROLLBACK TRANSACTION;
                    RETURN;
                END
                ELSE
                BEGIN
                    -- Reassign created_by fields
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

                    DELETE FROM [dbo].[Users]
                    WHERE [id] IN (SELECT [id] FROM DELETED);
                END
            END;
            """,
            reverse_sql="""
            DROP TRIGGER [before_user_delete];
            """
        ),
    ]
