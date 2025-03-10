USE pjw_db;
GO

-- Create the Users table
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    user_role VARCHAR(10) NOT NULL CHECK (user_role IN ('Admin','Lead','User')),
    created_at DATETIME2 DEFAULT GETDATE()
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
    FOREIGN KEY (created_by) REFERENCES Users(user_id) 
        ON UPDATE CASCADE --  If user deleted, reassigned to admin
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
    project_id INT NOT NULL,
    collaborator_id INT NOT NULL,
    PRIMARY KEY (project_id, collaborator_id),
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
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) 
        ON DELETE CASCADE, -- If project deleted, linked data also deleted
    FOREIGN KEY (assigned_to) REFERENCES Users(user_id) 
        ON DELETE SET NULL, --  If user deleted, it remains
    FOREIGN KEY (created_by) REFERENCES Users(user_id) 
        ON UPDATE CASCADE --  If user deleted, reassigned to admin
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
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) 
        ON DELETE CASCADE ON UPDATE CASCADE, -- If project deleted, linked data also deleted
    FOREIGN KEY (created_by) REFERENCES Users(user_id) 
        ON UPDATE CASCADE --  If user deleted, reassigned to admin
);

-- Create the Task_Deliverables junction table for Many-to-Many relationship
CREATE TABLE Task_Deliverables (
    task_id INT NOT NULL,
    deliverable_id INT NOT NULL,
    PRIMARY KEY (task_id, deliverable_id),
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id) 
        ON DELETE CASCADE ON UPDATE CASCADE, 
    FOREIGN KEY (deliverable_id) REFERENCES Deliverables(deliverable_id) 
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Create the Updates table
CREATE TABLE Updates (
    update_id INT IDENTITY(1,1) PRIMARY KEY,
    project_id INT NOT NULL,
    update_text VARCHAR(MAX) NOT NULL,
    created_by INT NOT NULL,
    created_at DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (project_id) REFERENCES Projects(project_id) 
        ON DELETE CASCADE ON UPDATE CASCADE, -- If project deleted, linked data also deleted
    FOREIGN KEY (created_by) REFERENCES Users(user_id) 
        ON UPDATE CASCADE --  If user deleted, reassigned to admin
);

-- Create the AuditLogs table
CREATE TABLE AuditLogs (
    log_id INT IDENTITY(1,1) PRIMARY KEY,
    user_id INT NOT NULL,
    act VARCHAR(MAX) NOT NULL,
    audit_time DATETIME2 DEFAULT GETDATE(),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) 
        ON DELETE SET NULL ON UPDATE CASCADE --  If user deleted, it remains
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
    SELECT TOP 1 @fallback_admin = user_id FROM Users WHERE user_role = 'Admin';

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
        WHERE created_by IN (SELECT user_id FROM DELETED);

        UPDATE Tasks
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT user_id FROM DELETED);

        UPDATE Deliverables
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT user_id FROM DELETED);

        UPDATE Updates
        SET created_by = @fallback_admin
        WHERE created_by IN (SELECT user_id FROM DELETED);
        
        DELETE FROM Users
        WHERE user_id IN (SELECT user_id FROM DELETED);
    END
END;
GO