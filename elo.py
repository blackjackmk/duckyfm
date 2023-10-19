import mysql.connector

mydb = mysql.connector.connect(
  host="185.253.218.123",
  user="wwmdhvjb_student",
  password="dzikaszyszk@2024",
  database="wwmdhvjb_duckyfm"
)


mycursor = mydb.cursor()
#mycursor.execute("CREATE TABLE users (name VARCHAR(27), surname VARCHAR(51))")

