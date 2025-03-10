USE pjw_db;
GO

-- Create the Users table
CREATE TABLE Users (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL UNIQUE,
    user_role VARCHAR(10) NOT NULL CHECK (user_role IN ('Admin','Lead','User')),
    is_superuser BIT NOT NULL DEFAULT 0, -- If True, user has all permissions without explicitly assigning them
    is_staff BIT NOT NULL DEFAULT 0, -- Typically set for staff or administrative roles.
    is_active BIT NOT NULL DEFAULT 1, -- If False, user account is considered inactive (cannot log in).
    -- The date/time this user record was originally created.
    date_joined DATETIME2 NOT NULL DEFAULT GETDATE(),
    last_login DATETIME2 NULL  -- Tracks last time user logged in (null until first login)
);

-- Create the Projects table
CREATE TABLE Projects (
    project_id INT IDENTITY(1,1) PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    proj_describe VARCHAR(MAX),
    start_date DATE,
    end_date DATE,
    proj_status VARCHAR(15) NOT NULL CHECK (proj_status in ('Not Started', 'In Progress', 'Completed', 'On Hold')),
    created_by INT NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    -- Removed ON UPDATE CASCADE referencing Users to avoid cycles
    FOREIGN KEY (created_by) REFERENCES Users(id)
);

-- Create the Collaborators table
CREATE TABLE Collaborators (
    collaborator_id INT IDENTITY(1,1) PRIMARY KEY,
    collab_name VARCHAR(100) NOT NULL,
    collab_describe VARCHAR(MAX),
    is_funder BIT NOT NULL DEFAULT 0, 
    created_at DATETIME2 DEFAULT GETDATE()
);

-- Create the Project_Collaborators junction table for Many-to-Many relationship
CREATE TABLE Project_Collaborators (
    projcollab_id INT IDENTITY(1,1) PRIMARY KEY,      -- New surrogate PK
    project_id INT NOT NULL,
    collaborator_id INT NOT NULL,
    UNIQUE (project_id, collaborator_id),             -- Preserves uniqueness of the pair

    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (collaborator_id) REFERENCES Collaborators(collaborator_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the Tasks table
CREATE TABLE Tasks (
    task_id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    task_name VARCHAR(100) NOT NULL,
    assigned_to INT,
    task_status VARCHAR(15) NOT NULL CHECK (task_status in ('Not Started', 'In Progress', 'Completed')),
    task_priority VARCHAR(10) NOT NULL CHECK (task_priority in ('Low', 'Medium', 'High')) DEFAULT 'Medium',
    due_date DATE,
    created_at DATETIME2 DEFAULT GETDATE(),
    created_by INT NOT NULL,
    -- Keep ON DELETE CASCADE so tasks are removed if project is deleted
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
        ON DELETE CASCADE,
    -- Keep ON DELETE SET NULL so if a user is deleted, assigned_to becomes NULL
    FOREIGN KEY (assigned_to) REFERENCES Users(id)
        ON DELETE SET NULL,
    -- Removed ON UPDATE CASCADE referencing Users to avoid cycles
    FOREIGN KEY (created_by) REFERENCES Users(id)
);

-- Create the Deliverables table
CREATE TABLE Deliverables (
    deliverable_id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    deliverable_name VARCHAR(100) NOT NULL,
    deliverable_describe VARCHAR(MAX),
    deliverable_status VARCHAR(15) NOT NULL CHECK (deliverable_status in ('Not Started', 'In Progress', 'Completed', 'On Hold')),
    created_at DATETIME2 DEFAULT GETDATE(),
    created_by INT NOT NULL,
    -- Keep ON DELETE CASCADE so deliverables are removed if project is deleted
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    -- Removed ON UPDATE CASCADE referencing Users to avoid cycles
    FOREIGN KEY (created_by) REFERENCES Users(id)
);

-- Create the Task_Deliverables junction table for Many-to-Many relationship
CREATE TABLE Task_Deliverables (
    taskdeliv_id INT IDENTITY(1,1) PRIMARY KEY,   -- New surrogate PK
    task_id INT NOT NULL,
    deliverable_id INT NOT NULL,
    UNIQUE (task_id, deliverable_id),            -- Preserves uniqueness of the pair

    /*
      CHANGE #1: Remove ON DELETE CASCADE from task_id to prevent multiple paths.
      If you delete a Task, remove the link in this table manually or via triggers.
      OR you can do ON DELETE CASCADE for task_id and no action for deliverable_id;
      the key is that both references can't have ON DELETE CASCADE if it leads back
      to a shared parent (Projects, etc.). One side must "break" the cascade path.
    */
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id)
        ON DELETE NO ACTION,
        
    /*
      CHANGE #2: Keep ON DELETE CASCADE for deliverable_id so that if a Deliverable
      is deleted, the linking record is also removed. This is just a design choice.
      If you prefer the opposite, swap the cascade with the task_id side.
    */
    FOREIGN KEY (deliverable_id) REFERENCES Deliverables(deliverable_id)
        ON DELETE CASCADE
);

-- Create the Updates table
CREATE TABLE Updates (
    update_id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    update_text VARCHAR(MAX) NOT NULL,
    created_by INT NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    -- Keep ON DELETE CASCADE so updates are removed if project is deleted
    FOREIGN KEY (project_id) REFERENCES Projects(project_id)
        ON DELETE CASCADE ON UPDATE CASCADE,
    -- Removed ON UPDATE CASCADE referencing Users to avoid cycles
    FOREIGN KEY (created_by) REFERENCES Users(id)
);

-- Create the AuditLogs table
CREATE TABLE AuditLogs (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    id INT NOT NULL,
    act VARCHAR(MAX) NOT NULL,
    audit_time DATETIME2 DEFAULT GETDATE(),
    -- Removed ON UPDATE CASCADE referencing Users to avoid cycles
    FOREIGN KEY (id) REFERENCES Users(id)
        ON DELETE NO ACTION
);
GO

-- Trigger to reassign project, deliverable, task, update to admin if created user is deleted
CREATE TRIGGER before_user_delete
ON Users
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @fallback_admin INT;

    -- Find an Admin user to take over ownership
    SELECT TOP 1 @fallback_admin = id 
    FROM Users 
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
        -- Reassign created_by fields to the fallback admin
        UPDATE Projects
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT id FROM DELETED);

        UPDATE Tasks
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT id FROM DELETED);

        UPDATE Deliverables
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT id FROM DELETED);

        UPDATE Updates
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT id FROM DELETED);
        
        DELETE FROM Users
        WHERE id IN (SELECT id FROM DELETED);
    END
END;
GO
