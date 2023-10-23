import sqlite3
import os

if os.path.isfile("dzika_szyszka.jpg"):
  
    #database connect
    conn = sqlite3.connect("duckybase.db")#if don't exist - create
    db = conn.cursor()
    

    #db.execute("INSERT INTO trades ('dateoftrade', 'hour_conclusion', 'min_conclusion', 'global_conclusion', 'priceatsix') VALUES ( ?, ?, ?, ?, ?)", (d1, houravg, minavg, conclusion, priceatsix))
    #conn.commit()
    
    

#wykrzaczacz    
else:
    exit(1)






