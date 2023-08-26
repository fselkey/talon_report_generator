
# import necessary packages
from flask import session
from flask_session import Session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException

import time
import settings
import cursor

driver = None

def save_images() :

   global driver
   driver = session['driver']

   ## SCROLL TO THE TOP OF IMAGES PAGE OR ELSE YOU WON'T FIND NO SUBMIT BUTTON
   driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.CONTROL + Keys.HOME)
   time.sleep(0.1)
   driver.find_element(by=By.TAG_NAME, value='body').send_keys(Keys.CONTROL + Keys.HOME)

   #save_image_changes_button = driver.find_element_by_xpath("/html/body/form[2]/div[1]/input")

   try :
      save_image_changes_button = driver.find_element(by=By.CLASS_NAME, value="sgl_css_submit")
      save_image_changes_button.click()
   except NoSuchElementException as exception :
      print ("SAVE IMAGE BUTTON NOT FOUND!!")

      save_image_changes_button = driver.find_element_by_xpath("/html/body/form[2]/div[1]/input")
      save_image_changes_button.click()
   except ElementNotInteractableException as exception :
      print ("SAVE IMAGE BUTTON NOT INTERACTABLE!!")
      save_image_changes_button = driver.find_element_by_xpath("/html/body/form[2]/div[1]/input")

      save_image_changes_button.click()

   session['driver'] = driver


def fix_images() :

   global driver

   driver = session['driver']

   url = settings.base_url+'gets/image_add.php?reportid='+str(session['report_id'])
   driver.get(str(url))
   driver.maximize_window()


   for idx, image in enumerate(session['img_files']) :
      
      cmdStr = "SELECT * FROM gets.timg WHERE reportid='"+str(session['report_id'])+"' AND file='"+image+"';"
      cursor.cur.execute(cmdStr)
      saved_image = cursor.cur.fetchall()
      #saved_image = cursor.execute(cmdStr)
      print('FOUND IMAGE FILE: ', saved_image)
      imgid = saved_image[0][0]
      inode = saved_image[0][1]
      ifile = saved_image[0][2].strip(".JPG | .PNG")

      print("IMGID: ", imgid)
      print("INODE: ", inode)
      print("IMAGE FILE NAME: ", ifile)
      print('IMG SESSION INDEX: ', str(idx))
      print('IMG SESSION TITLE: ', str(session['img_titles'][idx]))

      # Image title
      title_name = "title_"+str(inode)
      title_element = driver.find_element(by=By.NAME, value=title_name)
      title_element.clear()
      title_element.send_keys(str(session['img_titles'][idx]))


      # Report Section
      sectid_name = "sectid_"+str(inode)
      sectid_element = driver.find_element_by_xpath("//*[@name='"+str(sectid_name)+"']/option["+str(int(session['img_sectids'][idx])+1)+"]")
      sectid_element.click()

      #time.sleep(1)

      # Number of Columns
      cols_name = "cols_"+str(inode)
      cols_element = driver.find_element_by_xpath("//*[@name='"+str(cols_name)+"']/option["+session['img_cols'][idx]+"]")
      cols_element.click()
      
      #time.sleep(1)

      dord_number = session['img_dords'][idx]

      if str(dord_number) == '0' :
         dord_number = '1'
         print('DORD NUMBER WAS 0, NOW IT IS: ', dord_number)
         print('DORD NUMBER WAS 0, NOW IT IS: ', dord_number)
         print('DORD NUMBER WAS 0, NOW IT IS: ', dord_number)
         print('DORD NUMBER WAS 0, NOW IT IS: ', dord_number)
         print('DORD NUMBER WAS 0, NOW IT IS: ', dord_number)

      # Display Order
      dord_name = "dord_"+str(inode)
      dord_element = driver.find_element_by_xpath("//*[@name='"+str(dord_name)+"']")
      dord_element.click()
      print('SETTIG DORD WITH XPATH: ', "//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")
      print('SETTIG DORD WITH XPATH: ', "//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")
      print('SETTIG DORD WITH XPATH: ', "//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")
      print('SETTIG DORD WITH XPATH: ', "//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")
      print('SETTIG DORD WITH XPATH: ', "//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")
      print('SETTIG DORD WITH XPATH: ', "//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")

      dord_select_element = driver.find_element_by_xpath("//*[@name='"+str(dord_name)+"']/option["+dord_number+"]")
      dord_select_element.click()

      #time.sleep(1)

      # Image Description
      description_name = "ecomm_"+str(inode)
      description_element = driver.find_element(by=By.NAME, value=description_name)
      description_element.clear()
      description_element.send_keys(session['img_descriptions'][idx])

   session['driver'] = driver
   save_images()

