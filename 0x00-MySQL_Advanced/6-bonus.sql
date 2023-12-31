-- creates a stored procedure that corrects a table called users
DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus (user_id INT, project_name VARCHAR(255), score FLOAT)
BEGIN
    DECLARE project_count INT;

    SET project_count = (
        SELECT COUNT(*) FROM projects WHERE name = project_name
    );

    IF project_count = 0 THEN
        INSERT INTO projects(name)
	VALUES (project_name);
    END IF;
    INSERT INTO corrections(user_id, project_id, score)
    VALUES (user_id, (SELECT id FROM projects WHERE name = project_name), score);
END $$
DELIMITER ;
