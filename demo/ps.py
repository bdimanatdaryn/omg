import psycopg2
import csv

conn=psycopg2.connect(
    host="localhost",
    database="phonebook_db",
    user="postgres",
    password="2008"
)
cur=conn.cursor()

cur.execute("""
    CREATE TABLE elif NOT EXISTS phonebook(
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20)
)
""")

conn.commit()

print("1 - Add from console")
print("2 - Upload from CSV")
print("3 - Show contacts")
print("4 - Update")
print("5 - Search")
print("6 - Delete")

choise=input("Choose:")

#2.1
if choise == "1":
    name=input("Name: ")
    phone = input("Phone: ")

    cur.execute(
            "INSERT INTO phonebook (name,phone) VALUES (%s,%s)",
            (name,phone)
    )
    conn.commit()
    print("Added!") 

#2.2
elif choise == "2":
    with open("contacts.csv","r") as file:
        reader=csv.reader(file)
        for row in reader:
            cur.execute(
                "INSERT INTO phonebook (name,phone) VALUES (%s,%s)",(row[0],row[1])
            )
        conn.commit()
        print("CSV uploaded!")

#3
elif choise == "3":
    cur.execute("SELECT * FROM phonebook")
    rows=cur.fetchall()
    for row in rows:
        print(row)

#4
elif choise == "4":
    name = input("Enter name to update: ")
    new_phone = input("New phone: ")

    cur.execute("UPDATE phonebook SET phone=%s WHERE name=%s",(new_phone,name))

    conn.commit()
    print("Updated!")

#5
elif choise == "5":
    name = input("Enter name to search: ")

    cur.execute("SELECT * FROM phonebook WHERE name=%s",(name,))
    rows = cur.fetchall()

    for row in rows:
        print(row)
#6
elif choise == "6":
    name = input("Enter name to delete: ")

    cur.execute(
        "DELETE FROM phonebook WHERE name=%s",
        (name,)
    )
    conn.commit()
    print("Deleted!")

cur.close()
conn.close()