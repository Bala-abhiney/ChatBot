import sqlite3

# Connect to your database (change the file name if needed)
conn = sqlite3.connect('candidates.db')
cursor = conn.cursor()

# Query to list all tables
cursor.execute("SELECT score FROM submitted_emails;")
tables = cursor.fetchall()

print("Tables in the database:")
for table in tables:
    print(table[0])

conn.close()





# def clear_submitted_emails():
#     conn = sqlite3.connect("candidates.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM submitted_emails")
#     conn.commit()
#     conn.close()

# # Run the function
# clear_submitted_emails()
