

# import necessary packages
from flask import session
from flask_session import Session

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException, ElementNotInteractableException, NoSuchElementException

driver = None

def add_results_summary(row_id) :
   ##//*[@id="summ1_2928985"]/td[4]/input

   global driver
   
   driver = session['driver']

   ##*[@id="summ1_5158759"]/td[4]/input
   edit_summary_button_id = "summ1_"+str(row_id)
   edit_summary_button_xpath = "//*[@id='"+str(edit_summary_button_id)+"']/td[4]/input"
   driver.find_element_by_xpath(str(edit_summary_button_xpath)).click()

   edit_summary_textarea_id = "comm2_"+str(row_id)
   edit_summary_textarea_xpath = "//*[@id='"+str(edit_summary_textarea_id)+"']"
   summary_textarea = driver.find_element_by_xpath(str(edit_summary_textarea_xpath))
   summary_textarea.clear()
   summary_textarea.send_keys(session['quick_msg'])

   save_summary_button_id = "summ2_"+str(row_id)
   save_summary_button_xpath = "//*[@id='"+str(save_summary_button_id)+"']/td[5]/input"
   driver.find_element_by_xpath(str(save_summary_button_xpath)).click()

   session['driver'] = driver
