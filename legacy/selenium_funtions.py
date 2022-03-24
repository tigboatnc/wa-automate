

# Firebase Imports 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading
from google.api_core.datetime_helpers import DatetimeWithNanoseconds

# Selenium Imports 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

# Utility Imports
import copy
from urllib.parse import urlparse
import numpy as np
import pandas as pd
import re 
from pathlib import Path
import os
import time
from datetime import date
from datetime import timedelta
from datetime import datetime
import dateutil.parser as parser

import time

today = date.today()
cwd = os.getcwd()



# Default getter functions 
def F_SEARCH_2(driverVar,contact_number):

    driverVar.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.CONTROL + Keys.COMMAND + '//')
    time.sleep(1)


    FORM_HEADER_CLASS = '_1Jn3C' # Label Class
    FORM_CLASS = '_13NKt copyable-text selectable-text'

    formHeadingClassList = driverVar.find_elements(By.XPATH,f"//label[@class='{FORM_HEADER_CLASS}']")

    print(len(formHeadingClassList))


    if len(formHeadingClassList)==1:
        formHeadingClass = formHeadingClassList[0]
        formElementsList = formHeadingClass.find_elements(By.XPATH,f".//div[@class='{FORM_CLASS}']")

        print(len(formElementsList))

        if len(formElementsList)>0:
            formElement = formElementsList[0]
            formElement.click();
            formElement.clear();
            formElement.send_keys(f'{contact_number}')
            time.sleep(4)
            formElement.send_keys(Keys.RETURN)   

            
def F_SINGLE_SEND(driverVar,text_message):
    CHAT_HEADER_CLASS = '_1UWac _1LbR4'
    ALT_CHAT_HEADER_CLASS = '_1UWac _1LbR4 focused'
    CHAT_CLASS = '_13NKt copyable-text selectable-text'

    print('Trying Unfocussed')
    chatHeadingClassList = driverVar.find_elements(By.XPATH,f"//div[@class='{CHAT_HEADER_CLASS}']")
    if len(chatHeadingClassList)==0:
        print('Unfocussed failed, trying focussed;')
        chatHeadingClassList = driverVar.find_elements(By.XPATH,f"//div[@class='{ALT_CHAT_HEADER_CLASS}']")
    print(f'Length of Chat Header Div => {len(chatHeadingClassList)}')

    if len(chatHeadingClassList)==1:
        chatHeadingClass = chatHeadingClassList[0]
        chatElementsList = chatHeadingClass.find_elements(By.XPATH,f".//div[@class='{CHAT_CLASS}']")
        print(len(chatElementsList))
        if len(chatElementsList)>0:
            chatElement = chatElementsList[0]
            chatElement.click();
            time.sleep(1)
            chatElement.clear();
            chatElement.send_keys(f'{text_message}')
            time.sleep(2)
            chatElement.send_keys(Keys.RETURN)
            
def F_GET_NEW_MSG(driver):
    NEW_MESSAGE_BUBBLE_DIV = '_1pJ9J'
    
    
    BubbleList = driver.find_elements(By.XPATH,f"//div[@class='{NEW_MESSAGE_BUBBLE_DIV}']")

    OUTPUT = []

    for bubble in BubbleList:
    #   Click bubble to activate chat 
        bubble.click()
    #   Read message for current open user 
    
    #   Get user phon number and details 
        try:
            name,number = F_PROFILE_VIEWER(driver)
        except Exception:
            try:
                name,number = F_PROFILE_VIEWER(driver)
            except Exception:
                print('Error Resolving Name')
    
    #   Filter messages to only get unread messages 
    #   Return message list 


def F_PROFILE_VIEWER(driver):
    headers = driver.find_elements(By.XPATH,f"//header")
    for header in headers:
        header.click()
        time.sleep(1)

    headers = driver.find_elements(By.XPATH,f"//header")

    # validates if Contact Info page is open is open 
    headerValidator = [] 
    for header in headers:
        headerValidator.append(header.text)

    if 'Contact info' in headerValidator:
        print('Yes we are in contact info page: Verified')

    sections = driver.find_elements(By.XPATH,f"//section")

    if len(sections)>1:
        print('something is off') 
        return('ERROR: Section not synced with tested ')

    # First section under section 
    name_section = sections[0].find_elements(By.XPATH,f".//*")
    sectionTEXT = name_section[0].text
    print(sectionTEXT)
    time.sleep(3)
    sectionTEXT2 = sectionTEXT.split('\n')
    time.sleep(1)
    name = sectionTEXT2[1][1:]
    number = sectionTEXT2[0]
    

    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE)
    time.sleep(1)
    actions.perform()
    return name,number

def F_RESET_SOFT(driverVar,resetNo):
    # Soft reset of the state 
    time.sleep(3)
    F_SEARCH_2(driverVar,resetNo)
    time.sleep(3)

def F_RESET_HARD(driverVar,resetNo):
    # Soft reset of the state 
    driverVar.get("https://web.whatsapp.com/")
    time.sleep(7)
    F_SEARCH_2(driverVar,resetNo)
    time.sleep(3)
    
def F_TOGGLE_CLIPPY_ON(driverVar,trial=0):
    clipElements = driver.find_elements(By.XPATH,"//span[@data-testid='clip']")
    if len(clipElements)==1:
        clipElements[0].click()
        time.sleep(2)
        
        attachSpecificElement = driverVar.find_elements(By.XPATH,f"//span[@data-testid='{element_address}']")
        if len(attachSpecificElement)>0:
            print('[F_TOGGLE_CLIPPY_ON]-> Successfully, Opened Clippy')
            return 1
        else:
            print('[F_TOGGLE_CLIPPY_ON]->Error, in opening clippy, retrying','[try]: ',trial)
            F_TOGGLE_CLIPPY(driverVar,trial = trial + 1)
            
            
            
        
    else:
        if trial < 5 :
            print('[F_TOGGLE_CLIPPY_ON]-> Error, No Clip Element Found on Page,Trying Again','[try]: ',trial)
            F_TOGGLE_CLIPPY(driverVar,trial = trial + 1)
        else:
            return 0     

def F_GET_FILE(attachment_url):

    random.seed(datetime.now())
    file_name = str(random.random() * 100000).split('.')[0]
    if '.png' in document_link:
        file_format = 'png'
    elif '.pdf' in document_link:
        file_format = 'pdf'
    elif '.jpeg' in document_link:
        file_format = 'jpeg'
    elif '.jpg' in document_link:
        file_format = 'jpg'

    
    try:
        response = urllib.request.urlretrieve(attachment_url, f'./transaction_media/{file_name}.{file_format}')
        print(f'[F_GET_FILE]-> File Successfully Downloaded,stored at : {response[0]}')
        
        downloaded_file_local = response[0]
        downloaded_file_local_abs = os.getcwd() + downloaded_file_local[1:]
        downloaded_file_local_abs

        return downloaded_file_local_abs
    except Exception:
        print('[F_GET_FILE]-> File Not Available for download, Aborting')
        return 0 


    

def F_RECURSIVE_SEND(driverVar,contact_number,attachment_address,trial_number=0):
    
    F_SEARCH_2(driverVar,contact_number)
    F_TOGGLE_CLIPPY(driver)
    
    time.sleep(2)

    if '.pdf' in attachment_address:
        attachment_type = 'pdf'
    else:
        attachment_type = 'media'


    if attachment_type =='pdf':
        TYPE = 'pdf'
        element_address = 'attach-document'
    elif attachment_type =='media':
        TYPE = 'media'
        element_address = 'attach-image'

    attachSpecificElement = driverVar.find_elements(By.XPATH,f"//span[@data-testid='{element_address}']")

    if len(attachSpecificElement) == 1 : 
        attachInputElement = attachSpecificElement[0].find_elements(By.XPATH,f"..//input")
        
        if len(attachInputElement) == 1:
            
            attachInputElement[0].send_keys(downloaded_file_local_abs)
            time.sleep(5)
            actions = ActionChains(driverVar)
            actions.send_keys(Keys.ENTER)
            time.sleep(1)
            actions.perform()
            print( '[F_RECURSIVE_SEND]-> File Sent Successfully')
            return 1
            
        else:
            if trial_number>5:
                print('[F_RECURSIVE_SEND]-> Tries Exceeded 5, breaking')
                return 0
            else:
                print('[F_RECURSIVE_SEND]-> Found Attach-Specific Element(2), Cannot find attach input element Rerunning After Toggle ')
                F_RESET_HARD(driverVar,RESET_NO)
                F_RECURSIVE_SEND(driverVar,contact_number,attachment_address,trial_number = trial_number+1)
    

    else:
        if trial_number>5:
                print('[F_RECURSIVE_SEND]-> Tries Exceeded 5, breaking')
                return 0
        else:
            print('[F_RECURSIVE_SEND]-> Cannot Find Attach-Specific Element(1), Rerunning After Toggle ')
            F_RESET_HARD(driverVar,RESET_NO)
            F_RECURSIVE_SEND(driverVar,contact_number,attachment_address,trial_number = trial_number+1)