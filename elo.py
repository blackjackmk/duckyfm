import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="03220301513",
  database="mydatabase"
)


mycursor = mydb.cursor()
mycursor.execute("CREATE TABLE users (name VARCHAR(27), surname VARCHAR(51))")

