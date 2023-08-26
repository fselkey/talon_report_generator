
from flask import session
from flask_session import Session
import re

import cursor
import src.reader.reader as reader


def generate_report_sections() :

   cmdStr = "SELECT * FROM gets.tdata WHERE reportid='"+str(session['report_id'])+"' AND taskid='0' AND testid='0' ORDER BY sectid ASC LIMIT 50;"
   print("GET SECTIONS GETS TDATA CMD STRING: ", cmdStr)

   cursor.cur.execute(cmdStr)
   reports = cursor.cur.fetchall()
   cursor.con.commit()

   report_sections = []

   for report in reports :

      print('READER_TDATA GENERATE REPORT_SECTIONS SECTID', report[2])
      if report[2] != 1 :

         report_sections.append(report)

   session['report_sections'] = report_sections

def generate_test_rows() :

   section = session['section']
   section_id = int(section[2])
   task_id = int(section[3])

   session['sect_id'] = task_id + 1
   section_name = section[12]

   section_name = reader.uniform_name(section_name)
   session['section_name']=section_name

   print('GEN TEST NAMES SECTION ID: ', section_id)
   print('GEN TEST NAMES TASK ID: ', task_id)

   cmdStr = "SELECT * FROM gets.tdata WHERE reportid='"+str(session['report_id'])+"' AND sectid='"+str(section_id)+"' AND taskid='"+str(task_id)+"' LIMIT 50;"


   print('CMD STRING: ', cmdStr)
   cursor.cur.execute(cmdStr)
   rows = cursor.cur.fetchall()
   cursor.con.commit()

   print('GEN TEST NAMES ROWS: ', rows)

   test_rows = []
   for row in rows :
      if row[4] !=0 :
         test_rows.append(row)
      else :
         #IMPORTANT
         section_name = row[12]
         section_name = reader.uniform_name(section_name)
         session['section_name']=section_name

   session['test_rows'] = test_rows
   generate_report_sections()
