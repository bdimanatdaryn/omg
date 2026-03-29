import psycopg2

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008" 
)

cur=conn.cursor()

cur.execute(""" 
CREATE OR REPLACE FUNCTION test()
RETURNS VOID
AS $$
DECLARE
    i INT := 1;
BEGIN
    LOOP
        RAISE NOTICE 'Number: %', i;
        i := i + 1;

        IF i > 5 THEN
            EXIT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;
""")

conn.commit()


cur.execute("SELECT test();")
conn.commit()