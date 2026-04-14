import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)

cur=conn.cursor()

cur.execute("""
CREATE OR REPLACE PROCEDURE html(p_name TEXT)
            
""")