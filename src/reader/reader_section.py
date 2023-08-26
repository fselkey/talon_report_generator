
# import necessary packages
from flask import session
from flask_session import Session


import cursor


def get_report_ids() :

   cmdStr = "SELECT * FROM gets.thead WHERE snum='"+str(session['so_num'])+"' LIMIT 1;"
   cursor.cur.execute(cmdStr)

   thead_result = cursor.cur.fetchall()
   cursor.con.commit()

   print('THEAD SEARCH RESULT: ', thead_result)

   reportid = str(thead_result[0][0])
   session['report_id'] = reportid


   pnid = thead_result[0][11]
   session['pnid'] = pnid

   print('READER_SECTION FOUND REPORT ID: ', session['report_id'])
   print('READER_SECTION FOUND PART NUMBER ID: ', session['pnid'])


def get_part_number() :


   cmdStr = "SELECT * FROM norder.oline WHERE pnid='"+str(session['pnid'])+"' LIMIT 10;"
   print("GET PART NUMBER CMD STRING: ", cmdStr)

   cursor.cur.execute(cmdStr)

   oline_result = cursor.cur.fetchall()
   cursor.con.commit()

   print('OLINE RESULT PN: ', oline_result[0][19])

   part_number = oline_result[0][19]
   session['part_number'] = part_number

   print('READER_SECTION FOUND REAL PART NUMBER: ', part_number)


def get_intro_sections() :

   cmdStr = "SELECT * FROM gets.tdata WHERE reportid='"+str(session['report_id'])+"' AND sectid='1' AND testid='0' ORDER BY taskid ASC LIMIT 50;"
   print("GET SECTIONS GETS TDATA CMD STRING: ", cmdStr)

   cursor.cur.execute(cmdStr)
   sections = cursor.cur.fetchall()
   cursor.con.commit()

   print('READER_SECTION FOUND SECTIONS: ', sections)

   session['sections'] = sections
   print('READER_SECTION SAVED SESSION SECTIONS: ', session['sections'])


# configure_report_variables
def read_sections() :



   get_report_ids()

   #get_part_number()

   get_intro_sections()
   #get_test_rows()
