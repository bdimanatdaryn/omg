-- ADD PHONE
CREATE OR REPLACE PROCEDURE add_phone(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE phonebook
    SET phone = p_phone
    WHERE name = p_name;
END;
$$;

-- DELETE CONTACT
CREATE OR REPLACE PROCEDURE delete_contact(p_name TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM phonebook
    WHERE name = p_name;
END;
$$;

-- SEARCH FUNCTION
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT, email TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone, p.email
    FROM phonebook p
    WHERE p.name ILIKE '%' || p_pattern || '%'
       OR p.phone LIKE '%' || p_pattern || '%';
END;
$$;

-- MOVE TO GROUP
CREATE OR REPLACE PROCEDURE move_to_group(p_name TEXT, p_group TEXT)
LANGUAGE plpgsql
AS $$
DECLARE gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group;

    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group) RETURNING id INTO gid;
    END IF;

    UPDATE phonebook
    SET group_id = gid
    WHERE name = p_name;
END;
$$;

-- PAGINATION
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(name TEXT, phone TEXT, email TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT p.name, p.phone, p.email
    FROM phonebook p
    LIMIT p_limit OFFSET p_offset;
END;
$$;