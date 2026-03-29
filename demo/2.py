import psycopg2
import csv

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)
 
cur=conn.cursor()

cur.execute("CREATE TABLE if NOT EXISTS phonebook(id SERIAL PRIMARY KEY,name VARCHAR(100),phone VARCHAR(20))")
conn.commit()

cur.execute("""
CREATE OR REPLACE FUNCTION search_phonebook(pattern TEXT)
RETURNS TABLE (
    id INT,
    name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM phonebook
    WHERE phonebook.name ILIKE '%' || pattern || '%'
       OR phonebook.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;
""")

conn.commit()

pattern = input("Search: ")

cur.execute(
    "SELECT * FROM search_phonebook(%s)",
    (pattern,)
)

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()