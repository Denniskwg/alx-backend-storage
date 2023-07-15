-- creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a student
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser (user_id INT)
BEGIN
    DECLARE user_count INT DEFAULT 0;
    DECLARE scores INT DEFAULT 0;

    SET user_count = (
        SELECT COUNT(*) FROM corrections WHERE user_id = user_id
    );

    IF user_count > 1 THEN
        SET scores = (
          SELECT SUM(score) FROM corrections WHERE user_id = user_id
        );
	UPDATE users
            SET average_score = IF(user_count = 0, 0, scores / user_count)
	    WHERE id = user_id;
    ELSE
	SET scores = (
	    SELECT score FROM corrections WHERE user_id = user_id
	);
	 UPDATE users
	     SET average_score = IF(user_count = 0, 0, scores / user_count)
	     WHERE id = user_id;
    END IF;
END $$
DELIMITER ;
