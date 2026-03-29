import psycopg2 

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)

cur=conn.cursor()

cur.execute("""
CREATE OR REPLACE PROCEDURE odaryn(p_name TEXT) 
LANGUAGE plpgsql
AS $$
BEGIN
        DELETE FROM phonebook WHERE name=p_name;
END;
$$;
""")

conn.commit()

name=input("Name:")

cur.execute("""
CALL odaryn(%s)
""",(name,))
conn.commit()

cur.execute("""
SELECT * FROM phonebook
""")

rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()