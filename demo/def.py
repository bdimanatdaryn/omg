import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)
cur=conn.cursor()

cur.execute("""
CREATE TABLE filtered(id INT, name VARCHAR , phone VARCHAR)
""")
cur.execute("""
CREATE OR REPLACE FUNCTION sort()
RETURN QUERY(
id INT
name VARCHAR
phone VARCHAR         
            )
$$ AS
BEGIN
        SELECT * 
""")