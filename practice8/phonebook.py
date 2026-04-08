import psycopg2
from connect import connect


def call_upsert_contact():
    username = input("Enter username: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s)", (username, phone))
    conn.commit()

    print("Contact inserted/updated successfully!")

    cur.close()
    conn.close()


def search_by_pattern():
    pattern = input("Enter search pattern: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_by_pattern(%s)", (pattern,))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No matching contacts found.")

    cur.close()
    conn.close()


def show_paginated():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cur.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No contacts found.")

    cur.close()
    conn.close()


def delete_contact():
    value = input("Enter username or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s)", (value,))
    conn.commit()

    print("Contact deleted if it existed.")

    cur.close()
    conn.close()


def insert_many_from_console():
    n = int(input("How many contacts do you want to insert? "))

    usernames = []
    phones = []

    for _ in range(n):
        username = input("Enter username: ")
        phone = input("Enter phone: ")
        usernames.append(username)
        phones.append(phone)

    conn = connect()
    cur = conn.cursor()

    cur.execute("CALL insert_many_contacts(%s, %s)", (usernames, phones))
    conn.commit()

    print("Bulk insert completed! Check PostgreSQL notices for incorrect data.")

    cur.close()
    conn.close()


def main():
    while True:
        print("\n--- PHONEBOOK MENU (Practice 8) ---")
        print("1. Insert or update contact (procedure)")
        print("2. Search contacts by pattern (function)")
        print("3. Show contacts with pagination (function)")
        print("4. Delete contact by username or phone (procedure)")
        print("5. Insert many contacts (procedure)")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            call_upsert_contact()
        elif choice == "2":
            search_by_pattern()
        elif choice == "3":
            show_paginated()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            insert_many_from_console()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()