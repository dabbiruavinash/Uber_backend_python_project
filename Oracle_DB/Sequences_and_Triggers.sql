-- Sequences for ID generation
CREATE SEQUENCE user_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE vehicle_id_seq START WITH 1 INCREMENT BY 1;
CREATE SEQUENCE booking_id_seq START WITH 1 INCREMENT BY 1;

-- Trigger for automatic ID generation
CREATE OR REPLACE TRIGGER trg_users_id
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    IF :NEW.user_id IS NULL THEN
        :NEW.user_id := 'USR' || TO_CHAR(user_id_seq.NEXTVAL, 'FM000000');
    END IF;
END;
/

-- Similar triggers for other tables...