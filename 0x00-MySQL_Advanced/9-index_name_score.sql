-- creates an index on table names with first letter on name and score
CREATE INDEX idx_name_first_score ON names (name(1), score);
