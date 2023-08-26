
from flask_login import current_user

# import necessary packages
from flask import session
from flask_session import Session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException

import settings

driver = None
base_url = ''

def login() :


   global driver

   #driver = webdriver.Remote(command_executor=session['driver_session_url'], desired_capabilities={})
   #driver.session_id = session['driver_session_id']

   print('BASE URL WRITER LOGIN: ', base_url)

   url = base_url+'shared/log.php?'
   driver.get(str(url))
   driver.maximize_window()
   assert "Log In" in driver.title

   print('AUTH WRITER SESSION USER: ', session['user'])

   username = session['user']
   if username == '' :
      print('USERNAME IS ''!!!')
      username = current_user.username

   print('AUTH WRITER USERNAME: ', username)


   userElement = driver.find_element(by=By.NAME, value="login")
   userElement.clear()
   userElement.send_keys(str(username))
   #time.sleep(1)



   passElement = driver.find_element(by=By.NAME, value="freepass")
   passElement.clear()
   passElement.send_keys(str(session['pass']))
   #time.sleep(1)

   print('AUTH WRITER PASSWORD: ', session['pass'])


   driver.find_element(by=By.CLASS_NAME, value="sgl_css_submit").click()
   #time.sleep(1)

   url = base_url+'gets/report_view.php?reportid='+str(session['report_id'])
   driver.get(str(url))
   driver.maximize_window()


def init() :

   global driver, base_url

   base_url = settings.base_url

   print('BASE URL WRITER INIT: ', base_url)

   driver = webdriver.Chrome()

   login()

   session['driver'] = driver

   #session['driver_session_url'] = driver.command_executor._url
   #session['driver_session_id'] = driver.session_id
