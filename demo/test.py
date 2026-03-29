import psycopg2

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)

cur=conn.cursor()

cur.execute("""CREATE OR REPLACE PROCEDURE UPDT(d_phone TEXT,d_name TEXT)
            AS $$ 
            BEGIN
                IF EXISTS (SELECT 1 FROM phonebook WHERE name=d_name) THEN
                    UPDATE phonebook
                    SET phone=d_phone WHERE name=d_name;

                ELSE
                    INSERT INTO phonebook(name,phone) VALUES (d_name,d_phone);
                END IF;
            END;
            $$ LANGUAGE plpgsql;
            """)
conn.commit()
cur.close()
conn.close()