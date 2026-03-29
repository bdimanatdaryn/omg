import psycopg2

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008" 
)

cur=conn.cursor()
names = ['Ali', 'Beka', 'Nurs']
phones = ['+77001234567', '12345', '+77771234567']

cur.execute("""
CREATE OR REPLACE PROCEDURE ins(p_names TEXT[],p_phones TEXT[])
LANGUAGE plpgsql
AS $$
DECLARE
            i INT :=1;
BEGIN
            LOOP 
                IF i > array_length(p_names,1) THEN
                    EXIT;
                END IF;
                IF p_phones[i] ~ '^\\+7\\d{10}$' THEN
                    INSERT INTO phonebook(name,phone) VALUES(p_names[i],p_phones[i]);
                ELSE
                    RAISE NOTICE 'Wrong: %, %', p_names[i], p_phones[i];
                END IF;
                
                i := i+1;
            END LOOP;
END;
$$            
""")
conn.commit()

cur.execute("CALL ins(%s, %s);", (names, phones))
conn.commit()

# смотрим результат
cur.execute("SELECT * FROM phonebook;")
rows = cur.fetchall()

for row in rows:
    print(row)

cur.close()
conn.close()