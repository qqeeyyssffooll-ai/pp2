import csv
from connect import connect

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
            (username, phone)
        )
        conn.commit()
        print("Contact added successfully!")
    except Exception as e:
        conn.rollback()
        print("Error:", e)

    cur.close()
    conn.close()

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    cur.execute(
                        "INSERT INTO phonebook (username, phone) VALUES (%s, %s)",
                        (row["username"], row["phone"])
                    )
                except Exception as e:
                    conn.rollback()
                    print(f"Skipping {row['username']}: {e}")
                    continue

        conn.commit()
        print("CSV import completed!")
    except FileNotFoundError:
        print("CSV file not found!")

    cur.close()
    conn.close()

def update_contact():
    choice = input("Update by (1) username or (2) phone? ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        old_username = input("Enter current username: ")
        field = input("What do you want to update? (username/phone): ")

        if field == "username":
            new_username = input("Enter new username: ")
            cur.execute(
                "UPDATE phonebook SET username = %s WHERE username = %s",
                (new_username, old_username)
            )
        elif field == "phone":
            new_phone = input("Enter new phone: ")
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE username = %s",
                (new_phone, old_username)
            )

    elif choice == "2":
        old_phone = input("Enter current phone: ")
        field = input("What do you want to update? (username/phone): ")

        if field == "username":
            new_username = input("Enter new username: ")
            cur.execute(
                "UPDATE phonebook SET username = %s WHERE phone = %s",
                (new_username, old_phone)
            )
        elif field == "phone":
            new_phone = input("Enter new phone: ")
            cur.execute(
                "UPDATE phonebook SET phone = %s WHERE phone = %s",
                (new_phone, old_phone)
            )

    conn.commit()
    print("Contact updated!")

    cur.close()
    conn.close()

def query_contacts():
    print("1. Show all contacts")
    print("2. Search by exact username")
    print("3. Search by username pattern")
    print("4. Search by phone prefix")

    choice = input("Choose option: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM phonebook")
    elif choice == "2":
        username = input("Enter username: ")
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (username,))
    elif choice == "3":
        pattern = input("Enter name pattern: ")
        cur.execute("SELECT * FROM phonebook WHERE username ILIKE %s", ('%' + pattern + '%',))
    elif choice == "4":
        prefix = input("Enter phone prefix: ")
        cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", (prefix + '%',))
    else:
        print("Invalid option!")
        cur.close()
        conn.close()
        return

    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()

def delete_contact():
    choice = input("Delete by (1) username or (2) phone? ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        username = input("Enter username to delete: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (username,))
    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM phonebook WHERE phone = %s", (phone,))
    else:
        print("Invalid option!")
        cur.close()
        conn.close()
        return

    conn.commit()
    print("Contact deleted!")

    cur.close()
    conn.close()

def menu():
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert contact from console")
        print("2. Insert contacts from CSV")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            filename = input("Enter CSV filename: ")
            insert_from_csv(filename)
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()