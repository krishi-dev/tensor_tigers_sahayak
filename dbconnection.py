import mysql.connector

# Database connection details
DB_USER = "sahayak1"
DB_PASS = "O-RKDu&nhg)MoX*;"
DB_NAME = "sahayak"
HOST = "35.200.219.219"
PORT = 3306

# Connect to the database
try:
    connection = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )

    if connection.is_connected():
        print("✅ Connected to the database!")

        cursor = connection.cursor()
        table_name = "Class"  # Replace with actual table name

        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        print(f"\n📋 Data from '{table_name}':")
        for row in rows:
            print(row)

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")

