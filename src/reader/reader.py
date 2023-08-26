
# import necessary packages
from flask import session
from flask_session import Session

import cursor
import settings
import time
import re

import src.reader.reader_timg as reader_timg

same_pn_reportids = []


def reduce_summaries(summaries) :

   #print("LENGTH OF SIMILAR_SUMMARYS ARRAY: ", len(summaries))

   import collections

   for i, summary in enumerate(summaries) :
      summary_list = [item for item, count in collections.Counter(summaries).items() if count > len(summaries)/(2+i)]
      if len(summary_list) > 0 :
         #print('REDUCED LENGTH OF SIMILAR SUMMARYS:', summary_list)
         quick_msg = summary_list[0]
         session['quick_msg'] = quick_msg
         break


def conform_summary(summary) :

   iqty = 10
   pqty = 10

   tested_num_original = 'Tested '+str(iqty)+' '
   tested_num_new = 'Tested '+str(session['iqty'])+' '

   summary_tested = summary.replace(str(tested_num_original),str(tested_num_new))
         
   passed_num_original = 'Passed: '+str(pqty)+'.'
   passed_num_new = 'Passed: '+str(session['pqty'])+'.'

   summary_passed = summary_tested.replace(str(passed_num_original),str(passed_num_new))

   session['quick_msg'] = summary_passed

   return summary_passed


def enumerate_summary_rows(test_rows) :

   similar_summarys = []

   #print('check similar summarys iqty: ', session['iqty'])
   #print('check similar row: ', test_rows)
   #print('check similar summary: ', test_rows)


   for idx, test_row in enumerate(test_rows) :

      similar_summary = ''

      if test_row[23] is not None :

         similar_summary = test_row[23]
         similar_iqty = test_row[15]
         similar_pqty = test_row[16]

         tested_num_original = 'Tested '+str(similar_iqty)+' '
         tested_num_new = 'Tested '+str(session['iqty'])+' '

         similar_summary_tested = similar_summary.replace(str(tested_num_original),str(tested_num_new))
         
         passed_num_original = 'Passed: '+str(similar_pqty)+'.'
         passed_num_new = 'Passed: '+str(session['pqty'])+'.'

         similar_summary_passed = similar_summary_tested.replace(str(passed_num_original),str(passed_num_new))
         similar_summary_tested_split = similar_summary_passed.split(tested_num_new,2)

         if len(similar_summary_tested_split) > 1 :
            similar_summary = similar_summary_tested_split[1]
         else :
            similar_summary = similar_summary_tested_split[0]

         similar_summary_passed_split = similar_summary.split(passed_num_new,2)
         similar_summary = similar_summary_passed_split[0]

         similar_summary_datecodeless = similar_summary_passed.split('*',2)
         if len(similar_summary_datecodeless) > 1 :
            similar_summary = similar_summary_datecodeless[0]


         if str(similar_iqty) in str(similar_summary) :
            similar_summary = similar_summary.replace(str(similar_iqty), '')


         similar_summary = str(tested_num_new) + str(similar_summary) + '\n' + str(passed_num_new)
         similar_summarys.append(similar_summary)


         quick_msg = similar_summary
         session['quick_msg'] = quick_msg

   reduce_summaries(similar_summarys)


def check_same_pnid() :

   cmdStr = "SELECT * FROM gets.thead WHERE pnid='"+str(session['pnid'])+"' LIMIT 10;"
   #print('PNID THEAD CMDSTR', cmdStr)

   cursor.cur.execute(cmdStr)
   pnid_thead_results = cursor.cur.fetchall()
   cursor.con.commit()


   for idx, result in enumerate(pnid_thead_results) :

      if str(result[0]) != str(session['report_id']) :

         #print('REPORT ID WITH SAME PNID: ', result[0])

         reportid = result[0]
         same_pn_reportids.append(reportid)


   #print('same_pn_reportids RESULTS', same_pn_reportids)

   if len(same_pn_reportids) > 0 :
      get_summary_by_same_pnid_report_id()
   else :
      check_similar_summarys()





def get_summary_by_same_pnid_report_id() :

   #length_of_same = len(same_pn_reportids)
   #if length_of_same > 5 :
   #   length_of_same = 5
   #same_pn_reportids = same_pn_reportids[0:length_of_same]


   for idx, same_pn_report_id in enumerate(same_pn_reportids) :
   
      cmdStr = "SELECT * FROM gets.tdata WHERE reportid='"+str(same_pn_report_id)+"' AND tname='"+str(session['test_name'])+"' LIMIT 10;"
      # reportid='"+str(reportid)+"' AND
      #print('SAME PNID FOR TDATA SUMMARY CMD STRING: ', cmdStr)
      cursor.cur.execute(cmdStr)
      same_pnid_test_rows = cursor.cur.fetchall()
      cursor.con.commit()

      #print('SAME PNID TEST ROWS FROM GETS.TDATA: ', same_pnid_test_rows)

      enumerate_summary_rows(same_pnid_test_rows)


def check_similar_summarys() :
   #print('Checking for similar summarys...')
   #print('In the absence of information, LET THERE BE RECORDS!!')

   cmdStr = "SELECT * FROM gets.tdata WHERE tname='"+str(session['test_name'])+"' LIMIT 5000;"
   # reportid='"+str(reportid)+"' AND
   print('SIMILAR CMD STRING: ', cmdStr)
   cursor.cur.execute(cmdStr)
   similar_test_rows = cursor.cur.fetchall()
   cursor.con.commit()
   #print("SIMLIAR TEST ROWS: ", similar_test_rows)
   #print('SIMILAR TEST ROWS: ', similar_test_rows)

   if len(similar_test_rows) > 0 :
      enumerate_summary_rows(similar_test_rows)
   else :
      generate_quick_messages()


def get_test_rows() :

   cmdStr = "SELECT * FROM gets.tdata WHERE reportid='"+str(session['report_id'])+"' LIMIT 50;"


   #print('CMD STRING: ', cmdStr)
   cursor.cur.execute(cmdStr)
   rows = cursor.cur.fetchall()
   cursor.con.commit()

   test_rows = []

   for row in rows :
      if row[4] !=0 :
         test_rows.append(row)


   session['test_rows'] = test_rows


def uniform_name(row_name) :

   row_name = row_name.lower()
   print('UNIFORM NAME LOWER(): ', row_name)

   split_row_name = row_name.split('(')
   if len(split_row_name) > 1 :
      split_row_name = split_row_name[1].split(')')
   #row_name =  row_name.replace('GR1','').replace('GV1','').replace('GD1','').replace('GX1','').replace('GE1','').replace('Devices','').replace('devices','').replace('-', '').replace('Level C', '').replace('Test', '').replace('Basic', '')
   row_name =  row_name.replace('ge','').replace('gr1','').replace('gv1','').replace('gd1','').replace('gx1','').replace('ge1','').replace('devices','').replace('device','')
   row_name = row_name.replace('-', '').replace('Level C', '').replace(')','').replace('(','').replace('sow','').replace('test', '').replace('basic', '').replace('section','')
   row_name = row_name.replace('lot','').replace('%','').replace('>','').replace('<','').replace('=','').replace(',','').replace('see','').replace('appendix','')
   row_name = row_name.replace('extend','').replace('class','').replace('i/ii','').replace('capacitance','').replace('per','').replace('date','').replace('code','')
   row_name = row_name.replace('level','').replace('max','').replace('inspection','').replace('aql','').replace('of','').replace('sample','').replace('size','')
   row_name = row_name.replace('follow','').replace('kpac','').replace('increased','').replace('sampling','').replace('plan','').replace('2x','')
   row_name = row_name.replace('ac','').replace('dc','').replace('and','').replace('functional','').replace('functions','').replace('function','')
   row_name = row_name.replace('pieces','').replace('piece','').replace('nondestructive','').replace('destructive','')
   row_name = row_name.replace('all','').replace('switching','').replace('table','').replace('ëšc','').replace('ta','').replace('ta','')
   
   row_name = ' '.join([x for x in row_name.split() if len(x)>1])

   #print('UNIFORM NAMES replace section name: ', row_name)

   row_name = re.sub(r'[0-9\.]+', '', row_name)
   #print('UNIFORM NAMES re section name: ', row_name)

   row_name = ' '.join([x for x in row_name.split() if len(x)>1])


   row_name = row_name.strip()
   #print('UNIFORM NAMES strip section name: ', row_name)

   session['row_name']=row_name
   #print('UNIFORM NAMES section name: ', session['row_name'])

   row_name = re.sub(r'[0-9\.]+', '', row_name)
   #print('UNIFORM NAMES re section name: ', row_name)

   row_name = row_name.strip()
   #print('UNIFORM NAMES strip section name: ', row_name)

   return row_name



def generate_quantity() :
   
   cmdStr = "SELECT * FROM norder.oline WHERE onum='"+str(session['so_num'])+"' LIMIT 50;"

   print('CMD STRING: ', cmdStr)
   cursor.cur.execute(cmdStr)
   rows = cursor.cur.fetchall()
   cursor.con.commit()

   #print("GENERATE QUANTITY FOUND ROWS: ", rows)

   sections = session['sections']

   for row in rows :

      row_name = row[21]
      row_qty = row[22]

      row_name = uniform_name(row_name)

      # Required to allow for X-Ray to equal XRAY
      ## But this is currently breaking the curve tracer test
      #row_name = row_name.replace('-','')
      #row_names = row_name.split(' ')

      #if len(row_names) > 0 :
      #   row_name = row_names[0]

      section_name = uniform_name(session['section_name'])

      #print('GENERATE TEST QUANTITY: ', row_qty)
      #print('GENERATE QUANTITY SECTION NAME: ', section_name)
      #print('GENERATE QUANTITY OLINE ROW NAME: ', row_name)

      if section_name.lower() in row_name.lower() :

         session['iqty'] = row_qty
         session['pqty'] = row_qty
         session['fqty'] = 0


def get_test_row_ids() :

   cmdStr = "SELECT * FROM gets.tdata WHERE reportid='"+str(session['report_id'])+"' AND tname='"+str(session['test_name'])+"' LIMIT 5;"

   #print('CMD STRING: ', cmdStr)
   cursor.cur.execute(cmdStr)
   test_rows = cursor.cur.fetchall()
   cursor.con.commit()

   session['test_rows'] = test_rows

   #print("Test Rows: ", test_rows)
   test_row_id1 = test_rows[0][0]
   session['test_row_id1'] = test_row_id1

   if len(test_rows) > 1 :

      test_row_id2 = test_rows[1][0]
      session['test_row_id2'] = test_row_id2
   else :
      test_row_id2 = ''
      session['test_row_id2'] = test_row_id2

   #sect_id = test_rows[1][2]
   #session['sect_id'] = sect_id

   #print('TEST ROW 1: ', session['test_row_id1)']
   #print('TEST ROW 2: ', session['test_row_id2)']

def get_summary_row_id() :

   report_sections = session['report_sections']

   for idx, row in enumerate(report_sections) :
      #print('get_summary_row_id summary row id idx', idx)
      #print('get_summary_row_id summary row', row)

      section_name = session['section_name']
      #print('get_summary_row_id section_name', section_name)
      section_name = uniform_name(section_name)
      #print('get_summary_row_id uniform section_name', section_name)
      if section_name.lower() in row[12].lower() :

         session['summary_row_id'] = row[0]
         session['summary_sect_id'] =row[2]

         #print('get_summary_row_id READER FOUND SUMMARY SECTION ID SECTID!!!', row[2])

      #else :
         #print('get_summary_row_id THIS IS NOT THE SUMMARY ROW...')

   #print('get_summary_row_id summary section number id: ', session['summary_sect_id'])


def prep_quick_messages(messages) :

   quick_msgs = []
   original_quick_msgs = []

   for quick_msg in messages :

      pre_quick_msg = ''
      post_quick_msg = ''

      tested_split = quick_msg.split('Tested ')

      if(len(tested_split) > 1) :
         #print('QUICK MSG TESTED SPLIT LEN > 1: ',tested_split)

         pre_quick_msg = tested_split[0]

         tested_split = tested_split[1]
         #print('QUICK MSG TESTED SPLIT[1]: ',tested_split)

         tested_num_list = tested_split.split(' ')
         #print('QUICK MSG TESTED NUM SPLIT: ',tested_num_list)

         tested_num_list.pop(0)
         #print('QUICK MSG TESTED NUM LIST: ',tested_num_list)

         tested_string = ' '.join(tested_num_list)
         #print('TESTED STRING: ',tested_string)

         tested_string = "Tested "+str(session['iqty']) + ' ' + tested_string

      else :
         tested_string = tested_split[0]
         #print('ELSE TESTED STRING: ',tested_string)


      #print('QUICK MSG TESTED STRING: ',tested_string)


      passed_split = tested_string.split('Passed: ')
      #print('QUICK MSG PASSED SPLIT: ',passed_split)

      if(len(tested_split) > 1) :

         post_quick_msg = passed_split[1]

         post_quick_msg = post_quick_msg.split(' ')
         #print('QUICK MSG PASSED NUM SPLIT: ',post_quick_msg)

         post_quick_msg[0] = re.sub(r'[0-9\.]+', '', post_quick_msg[0])
         post_quick_msg[0] = post_quick_msg[0].replace('\n', '')
         
         post_quick_msg[0]

         #print('QUICK MSG PASSED NUM LIST: ',post_quick_msg)

         post_quick_msg = ' '.join(post_quick_msg)
         #print('POST PASSED STRING: ',post_quick_msg)

      else :
         post_quick_msg = ''

      passed_split = passed_split[0]

      passed_split = passed_split + ' Passed: ' + str(session['pqty']) + '.'

      #print('QUICK MSG PASSED SPLIT: ',passed_split)

      mod_string = passed_split

      if pre_quick_msg != '' :
         mod_string = pre_quick_msg + ' \n ' + mod_string
      if post_quick_msg != '' :
         mod_string = mod_string + ' \n ' + post_quick_msg

      quick_msgs.append(mod_string)
      original_quick_msgs.append(quick_msg)

   session['quick_msgs'] = quick_msgs
   session['original_quick_msgs'] = original_quick_msgs

   if session['quick_msg'] == '' :
      session['quick_msg'] = 'Sorry, we could not automatically generate a quick message for you today.'


   test_template = session['test_template']
   if test_template != '' :
      for template in settings.test_templates :
         if str(template.tag) == str(test_template) :

            qck_msg = conform_summary(template.summary)

            print('template.summary: ', template.summary)
            print('QUICK MESSAGE CONFORM SUMMARY: ', qck_msg)
            session['quick_msg'] = qck_msg


def generate_quick_messages() :

   quick_msgs = []

   #print('GENERATE QUICK MESSAGE TEST NAME: ', str(session['test_name']))


   cmdStr = "SELECT * FROM gets.quick_msg WHERE title='"+str(session['test_name'])+"' LIMIT 5;"
   #print('GENERATE QUICK MESSAGE COMMAND STRING: ', cmdStr)

   cursor.cur.execute(cmdStr)
   messages = cursor.cur.fetchall()
   cursor.con.commit()
   #print('GENERATE QUICK MESSAGE FOUND ROWS: ', messages)

   for message in messages :

      quick_msg = str(message[5])

      quick_msgs.append(quick_msg)

      session['quick_msgs'] = quick_msgs


def avengers_assemble(test_template) :

   print('THIS IS A CURVE TRACER TEST!!')




def generate_tdata() :

   quick_msgs = []
   test_templates = []
   image_templates = []

   generate_quantity()

   get_test_row_ids()

   get_summary_row_id()

   reader_timg.get_images()

   test_name = session['test_name'].replace('Test','').replace('TA','').replace('=','').replace('25ËšC','').strip().lower()

   test_template = session['test_template']

   print('TEST_TEMPLATE: ', test_template)

   #if 'curve tracer' in test_name :
      #session['test_template'] == 'ct'.
   
   if test_template != 'None' or test_template != '' :

      test_templates = settings.test_templates
      img_templates = settings.image_templates


      for i, template in enumerate(test_templates) :
         if template.tag == test_template :

            quick_msgs.append(template.summary)

            equip_template = str(template.asset)
            session['equipment_template'] = equip_template

      print('quick_msgs', quick_msgs)
      prep_quick_messages(quick_msgs)

      for i, image_template in enumerate(img_templates) :
         if image_template.tag == test_template :
            image_templates.append(image_template)
      print('image_templates', image_templates)

      session['image_templates'] = image_templates

   #if session['test_template'] == 'ct' :

   else :
      check_same_pnid()

      #print('NOT A CURVE TRACER TEST!!')