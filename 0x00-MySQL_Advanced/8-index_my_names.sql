-- creates an index on table names with first letter of name
DROP INDEX IF EXISTS idx_name_first;
CREATE INDEX idx_name_first ON names (SUBSTRING(name, 1, 1));
