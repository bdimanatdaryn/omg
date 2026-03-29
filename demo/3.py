import psycopg2

conn=psycopg2.connect(
        host="localhost",
        database="phonebook_db",
        user="postgres",
        password="2008" 
)

cur=conn.cursor()

cur.execute("""
CREATE OR REPLACE PROCEDURE add_or_update_user(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$;
""")
conn.commit()

name = input("Name: ")
phone = input("Phone: ")

cur.execute(
    "CALL add_or_update_user(%s, %s)",
    (name, phone)
)

conn.commit()

cur.close()
conn.close()