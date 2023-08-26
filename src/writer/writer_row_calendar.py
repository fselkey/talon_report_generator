
# import necessary packages
from flask import session
from flask_session import Session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from datetime import date

import settings

driver = None


def try_other_magic_num(num) :

   magicNum = 0
   if settings.prod == True:
      magicNum = 7+int(num)
   else :
      magicNum = 10+int(num)
   try :
      todays_xpath = "/html/body/div["+str(magicNum)+"]/table/thead/tr[2]/td[3]/div"
      print('TODAYS_XPATH: ', todays_xpath)
      driver.find_element_by_xpath(todays_xpath).click()
   except NoSuchElementException as exception :
      print ("magic num day not found")
   except ElementNotInteractableException as exception :
      print ("magic num day not interactable")


def try_magic_num(num) :

   magicNum = 0
   if settings.prod == True:
      magicNum = 8+int(num)
   else :
      magicNum = 11+int(num)

   try :
      todays_xpath = "/html/body/div["+str(magicNum)+"]/table/thead/tr[2]/td[3]/div"
      print('TODAYS_XPATH: ', todays_xpath)
      driver.find_element_by_xpath(todays_xpath).click()
   except NoSuchElementException as exception :
      print ("magic num day not found")
      try_other_magic_num(num)
   except ElementNotInteractableException as exception :
      print ("magic num day not interactable")
      try_other_magic_num(num)


def try_today(num) :
   try :
      today_button = driver.find_element_by_xpath('//td[@class="day today"]')
      today_button.click()
   except NoSuchElementException as exception :
      print ("day today not found")
      try_magic_num(num)
   except ElementNotInteractableException as exception :
      print ("day today not interactable")
      try_magic_num(num)

#day selected today
def try_selected_today() :
   try :
      today_button = driver.find_element_by_xpath('//td[@class="day"]')
      today_button.click()
   except NoSuchElementException as exception :
      print ("day not found")
   except ElementNotInteractableException as exception :
      print ("day not interactable")

def try_yesterday(yesterday) :
   try :
      yesterday_button = driver.find_element_by_xpath('//td[text()='+str(yesterday)+']')
      yesterday_button.click()
   except ElementNotInteractableException as exception :
      print ("CALENDAR DAY NOT INTERACTABLE")


def try_anchored_day() :
   try :
      anchor_button = driver.find_element_by_xpath('/html/body/div[12]/table/tbody/tr[4]/td[5]')
      anchor_button.click()
      try_today()

   except ElementNotInteractableException as exception :
      print ("anchor_button NOT INTERACTABLE")
      try_today()



def calendar_test_row(num, test_row_id) :

   global driver

   driver = session['driver']

   print('ENTER CALENDAR DATE PICKER!!!')

   # Open Calendar
   calendar_id = "tdat_trigger_"+str(test_row_id)
   calendar_xpath = "//*[@id='"+calendar_id+"']"
   driver.find_element_by_xpath(str(calendar_xpath)).click()

   print('CALENDAR_XPATH: ', calendar_xpath)

   # Click any date element
   ## FIX THIS TO SELECT TODAYS DATE
   todays_date = date.today()
   today = todays_date.day
   yesterday = str(int(today) -1)

   print('CALENDAR DATE TODAY', today)

   try_today(num)

   print('COMPLETED ADD CALENDAR')

   session['driver'] = driver

   print('COMPLETED ADD CALENDAR SESSION DRIVER')
