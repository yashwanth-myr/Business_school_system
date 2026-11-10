# import sqlite3

# # Connect to the database
# conn = sqlite3.connect("school.db")
# cursor = conn.cursor()

# # Check the schema of the Branches table
# cursor.execute("PRAGMA table_info(Branches);")
# columns = cursor.fetchall()

# # Display the schema
# for column in columns:
#     print(column)

# # Close the connection
# conn.close()

# import sqlite3

# def print_users():
#     conn = sqlite3.connect("school.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM Users")
#     users = cursor.fetchall()
#     for user in users:
#         print(user)
#     conn.close()

# print_users()

import sqlite3

def check_data():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    # Check Classes table
    cursor.execute("SELECT * FROM Classes")
    classes = cursor.fetchall()
    print("Classes:")
    for row in classes:
        print(row)

    # Check Students table
    cursor.execute("SELECT * FROM Students")
    students = cursor.fetchall()
    print("\nStudents:")
    for row in students:
        print(row)

    conn.close()

if __name__ == "__main__":
    check_data()