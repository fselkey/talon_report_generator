
# import necessary packages
import mariadb
import sys

import settings

cur = None
con = None
host = ''


def reconnect_db() :

   global host


   print('Reconnecting to MariaDB server... @', host)

   time.sleep(5)
   init()

def connect_db() :

   global cur, con, host

   print("Connecting to MariaDB server... @", host)

   # Connect to mariaDB Platform
   try:
      conn = mariadb.connect(
         user="fselkey",
         password="Fast#33Trees",
         host=host,
         port=3306
      )

   except mariadb.Error as e :
      print(f"Error connecting to MariaDB Platform")
      #sys.exit(1)
      reconnect_db()

   # Get Cursor
   cur = conn.cursor()
   con = conn



def init() :

   global host

   if settings.prod == True :
      host = 'gets1.gets'
      print('CURSOR USING PRODUCTION SERVER GETS1')
   else :
      host = 'gets1.gets'
      print('CURSOR USING DEVELOPMENT SERVER GETSDEV2')

   connect_db()


   
