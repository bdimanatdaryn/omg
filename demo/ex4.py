import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008" 
)

cur=conn.cursor()
cur.execute("DROP FUNCTION IF EXISTS dlimit(INT, INT);")
conn.commit()

cur.execute("""
CREATE OR REPLACE FUNCTION dlimit(p_limit INT,p_offset INT)
RETURNS TABLE(
id INT,
name VARCHAR,
phone VARCHAR)
AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM phonebook ORDER BY id LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;
"""
)

conn.commit()

limit=int(input("Limit:"))
offset=int(input("Offset:"))

cur.execute("""
SELECT * FROM dlimit(%s,%s)
""",(limit,offset)
)
rows = cur.fetchall()

for row in rows:
    print(row)

conn.commit()

cur.close()
conn.close()