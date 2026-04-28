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