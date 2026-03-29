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

print("1 - Upload from CSV")
print("2 - Add from console")
print("3 - Show contacts")
print("4 - Update")
print("5 - Search")
print("6 - Delete")

x=input("Select option:")

if x == "1":
    with open("contacts.csv","r") as file:

        reader=csv.reader(file)
        for i in reader:
            cur.execute("INSERT INTO phonebook (name,phone) VALUES (%s,%s)",(i[0],i[1]))
        conn.commit()
        print("Uploaded from CSV")

elif x == "2":
    name=input("Print name:")
    phone=input("Print phone:")

    cur.execute("INSERT INTO phonebook (name,phone) VALUES (%s,%s)",(name,phone))
    conn.commit()
    print("Values was uploaded")

elif x=="3":
    cur.execute("SELECT * FROM phonebook")
    row=cur.fetchall()
    for i in row:
        print(i)

elif x == "4":

    name=input("Print name:")
    new_phone=input("Update phone:")

    cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s",(new_phone,name))

    conn.commit()
    print("Updated!")

elif x == "5":
    name=input("Input name:")

    cur.execute("SELECT * FROM phonebook WHERE name=%s",(name,))
    rows=cur.fetchall()

    for i in rows:
        print(i)

elif x == "6":
    name = input("Input name to delete:")

    cur.execute("DELETE FROM phonebook WHERE name = %s",(name,))

    conn.commit()
    print("Deleted!")

cur.close()
conn.close()