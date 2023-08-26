
# import necessary packages
from flask import session
from flask_session import Session

import time

import settings
import src.writer.writer_auth as writer_auth
import src.writer.writer_image as writer_image
import src.writer.writer_row as writer_row
import src.writer.writer_summary as writer_summary


driver = None

def close_driver() :

   global driver
   
   #time.sleep(3)

   driver = session['driver']

   driver.close()

   session['driver'] = None

   print('COMPLETED DRIVER CLOSE')


def save_new_images() :

   global driver

   writer_auth.init()

   driver = session['driver']

   #from selenium.webdriver.common.action_chains import ActionChains
   #actions = ActionChains(driver)
   #actions.send_keys('i')
   #actions.perform()

   driver.find_element_by_tag_name('body').send_keys('i')
   driver.find_element_by_tag_name('body').send_keys('i')

   writer_image.save_images()

   close_driver()


def file_report() :

   global driver

   writer_auth.init()

   #time.sleep(5)

   print('COMPLETED WRITER AUTH INIT')

   writer_row.write_row(1, session['test_row_id1'])

   print('COMPLETED ADD ROW 1')

   #time.sleep(1)

   if session['test_row_id2'] != '' :
      writer_row.write_row(2, session['test_row_id2'])
      #time.sleep(1)

   print('COMPLETED ADD ROW 2')

   writer_summary.add_results_summary(session['summary_row_id'])

   print('COMPLETED ADD ROW SUMMARY')

   #time.sleep(1)
   writer_image.fix_images()

   close_driver()



