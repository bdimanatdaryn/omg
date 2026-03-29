import psycopg2

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008" 
)

cur=conn.cursor()

cur.execute("""
CREATE OR REPLACE FUNCTION ret_count()
RETURNS INT
AS $$
BEGIN
    RETURN (SELECT COUNT(*) FROM phonebook);
END;
$$ LANGUAGE plpgsql;""")

conn.commit()

cur.execute("SELECT ret_count();")


result = cur.fetchone()


print("Count:", result[0])

cur.close()
conn.close()