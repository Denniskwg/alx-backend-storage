-- Creates a trigger that decreases the quantity
-- of an item after adding a new order.
DROP TRIGGER IF EXISTS decrease_quantity_trigger;
DELIMITER $$
CREATE TRIGGER decrease_quantity_trigger
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
        SET quantity = quantity - NEW.quantity
        WHERE name = NEW.item_name;
END $$
DELIMITER ;
