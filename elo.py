import mysql.connector
import os

if os.path.isfile("dzika_szyszka.jpg"):
  
    mydb = mysql.connector.connect(
     host="185.253.218.123",
     user="wwmdhvjb_student",
     password="dzikaszyszk@2024",
     database="wwmdhvjb_duckyfm"
    )
    
    
    

#wykrzaczacz    
else:
    exit(1)






