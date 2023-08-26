

# import necessary packages
from flask import session
from flask_session import Session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException

from datetime import date

import settings
import src.writer.writer_row_calendar as writer_row_calendar

driver = None

def edit_test_row(test_row_id) :

   global driver

   # Edit test row
   driver.find_element_by_xpath("//*[@id='row1_"+str(test_row_id)+"']/td[10]/input").click()


def write_test_row(test_row_id) :

   global driver

   try :
      iqty_id = "iqty2_"+str(test_row_id)
      iqty_element = driver.find_element(by=By.ID, value=iqty_id)
      iqty_element.clear()
      iqty_element.send_keys(session['iqty'])
      print('ROW FOUND IQTY ELEMENT')
   except NoSuchElementException as exception :
      print('ROW FOUND NO IQTY ELEMENT, QUIT NOW!')
      return False
   
   try :

      pqty_id = "pqty2_"+str(test_row_id)
      pqty_element = driver.find_element(by=By.ID, value=pqty_id)
      pqty_element.clear()
      pqty_element.send_keys(session['pqty'])
      print('WE FOUND ELEMENT')
   except NoSuchElementException as exception :
      print('ROW FOUND NO PQTY ELEMENT, QUIT NOW!')
      return False

   try :

      fqty_id = "fqty2_"+str(test_row_id)
      fqty_element = driver.find_element(by=By.ID, value=fqty_id)
      fqty_element.clear()
      fqty_element.send_keys(session['fqty'])
      print('WE FOUND ELEMENT')
   except NoSuchElementException as exception :
      print('ROW FOUND NO FQTY ELEMENT, QUIT NOW!')
      return False

   return True

def add_row_summary(rowNum, test_row_id) :

   global driver

   if rowNum == 1 :
      msg_id = "comm2_"+str(test_row_id)
      msg_element = driver.find_element(by=By.ID, value=msg_id)
      msg_element.clear()
      msg_element.send_keys(session['quick_msg'])
      print('WE FOUND ELEMENT')
   else :
      return

def na_uncheck_mark(test_row_id) :

   global driver

   checkbox_id = "nota2_"+str(test_row_id)
   checkbox_element = driver.find_element(by=By.ID, value=checkbox_id)
   checkValue = checkbox_element.get_attribute("checked")
   if checkValue :
      print('UNCHECKING THE CHECKBOX!!!')

      checkbox_element.click()
   else :
      print('LEAVING THE CHECKBOX UNCHECKED!!!')
      return

def asset_test_row(test_row_id) :

   global driver

   asset_tags = session['asset_tags']
   
   if len(asset_tags) == 0 :
      return


   # Before clicking the link first store the window handle as
   window_before = driver.window_handles[0]

   # Click add/change/del equipment
   equipment_button_id = "row2_"+str(test_row_id)
   equipment_button_xpath = "//*[@id='"+str(equipment_button_id)+"']/td[8]/input[3]"
   driver.find_element_by_xpath(str(equipment_button_xpath)).click()

   # after clicking the link store the window handle of newly opened window as
   window_after = driver.window_handles[1]

   # then execute the switch to window method to move to newly opened window
   driver.switch_to.window(window_after)

   # Type equipment tags into input area
   remove_equipment_element = driver.find_element_by_xpath("//*[@id='titl_0']")
   remove_equipment_element.click()

   # Switch back to equipment tags
   print('SWITCHING TO ORIGINAL DRIVER WINDOW BEFORE')
   driver.switch_to.window(window_before)
   
   tags = asset_tags.split(',')

   print('length of asset tags: ', len(tags))

   for i, tag in enumerate(tags) :

      tag = tag.strip()

      # Before clicking the link first store the window handle as
      window_before = driver.window_handles[0]

      # Click add/change/del equipment

      equipment_button_id = "row2_"+str(test_row_id)
      equipment_button_xpath = "//*[@id='"+str(equipment_button_id)+"']/td[8]/input[3]"
      driver.find_element_by_xpath(str(equipment_button_xpath)).click()

      # after clicking the link store the window handle of newly opened window as
      window_after = driver.window_handles[1]

      # then execute the switch to window method to move to newly opened window
      driver.switch_to.window(window_after)

      # Type equipment tags into input area
      addEquipElement = driver.find_element_by_xpath("/html/body/div[3]/form/input[1]")
      addEquipElement.send_keys(str(tag))

      driver.find_element_by_xpath("/html/body/div[3]/form/input[2]").click()

      #time.sleep(1)

      if get_status(driver) == True :

         print('GET STATUS DRIVER RETURNED TRUE')
         #atag_num = int(tag) + 2
         #select_equip_id = "atag_"+str(atag_num)
         #select_equip_xpath = "//*[@id='"+str(select_equip_id)+"']"
         #driver.find_element_by_xpath(str(select_equip_xpath)).click()
         driver.find_element_by_class_name('sgl_css_rep1').click()

      #time.sleep(1)
      print('SWITCHING TO ORIGINAL DRIVER WINDOW BEFORE')
      driver.switch_to.window(window_before)
      #time.sleep(1)


def get_status(driver) :
   try:
      driver.current_url
      print('Selenium is running')
      return True
   except WebDriverException:
      print('Selenium was closed')
      return False


def save_test_row(test_row_id) :

   global driver

   # Save intro row of test data
   save_button_id = "row2_"+str(test_row_id)
   save_button_xpath = "//*[@id='"+str(save_button_id)+"']/td[9]/input"
   driver.find_element_by_xpath(save_button_xpath).click()
   #time.sleep(1)






def write_row(rowNum, test_row_id) :

   global driver

   driver = session['driver']

   edit_test_row(test_row_id)


   second_row = write_test_row(test_row_id)

   if second_row :

      na_uncheck_mark(test_row_id)

      writer_row_calendar.calendar_test_row(rowNum, test_row_id)

      asset_test_row(test_row_id)

   add_row_summary(rowNum, test_row_id)

   save_test_row(test_row_id)

   session['driver'] = driver
