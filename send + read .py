#!/usr/bin/env python
# coding: utf-8

# # 1. Setup 

# In[ ]:



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
import urllib.request
import random


import time

today = date.today()
cwd = os.getcwd()


# ## 1.1 Set up technician variables 

# In[ ]:


CLIENT_ID = u'YIJ3bLzUXlubsxnDPnDR' # ID of client 
PROJECT_ID = u'BOuyALnDYmDHSBW7kAZm' # ID of the project 
RESET_NO = '9953674770'


# ## 1.2 Set up `FIREBASEAGENT`

# In[ ]:


firebase_project_id = 'tpc-dev-5330f'
# Use the application default credentials
cred = firebase_admin.credentials.Certificate('./secret/tpc-dev-5330f-firebase-adminsdk-2p698-e13719db26.json')

firebase_admin.initialize_app(cred, {
  'projectId': firebase_project_id,
})

db = firestore.client()


# In[ ]:


doc_ref = db.collection(u'clients').document(CLIENT_ID).collection(u'projects').document(PROJECT_ID).collection('wa-queue')


# In[ ]:





# In[ ]:





# In[ ]:





class CLASS_FIREBASEAGENT:
    
    queue_length = 0 

    def firebase_update(self,new_data):
        if new_data['id'] not in self.queue_ids:
            
            self.queue.append(new_data)
            self.queue_ids.append(new_data['id'])
            
            self.queue_length = len(self.queue)
        else:
            print('Tried to read - unknown Queue ID')

    def server_update(self,task_id,update):
        if update == 'done':
            self.db.collection(u'clients').document(CLIENT_ID).collection(u'projects').document(PROJECT_ID).collection('wa-queue').document(task_id).delete()
            print(f'[CLASS_FIREBASEAGENT]-> Deleting Task From Firebase {task_id}')
            indexOfFileInQueue = next((i for i, item in enumerate(self.queue) if item["id"] == task_id), None)
            indexOfFileInQueueIds = self.queue_ids.index(task_id)
            del self.queue[indexOfFileInQueue]
            del self.queue_ids[indexOfFileInQueueIds]
            self.queue_length = len(self.queue)
    
    def append(self,data):
#         print(str(data))
#         text_file = open("sample.txt", "w")
#         n = text_file.write(str(data))
#         text_file.close()t
        print('IDK WHAT HAPPENS HERE')
        print('FIND OUT!!!!!!')

        
        
    
    def __init__(self,database_client):
        self.queue = [] 
        self.queue_ids = []
        self.db = database_client
 
    


# In[ ]:


# Create an Event for notifying main thread.
callback_done = threading.Event()
# MAIN VARIABLE : Clean after use 
FIREBASEAGENT = CLASS_FIREBASEAGENT(db)

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    for doc in col_snapshot:
        current = doc.to_dict()
        current['id'] = doc.id
        
        FIREBASEAGENT.firebase_update(current)
    callback_done.set()
    

col_query = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').where(u'processed', u'==', False)

# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)


# ## 1.3 Set up `PHONEBOOKAGENT`

# In[ ]:


guest_reference = []
guests = db.collection(u'clients').document(CLIENT_ID).collection(u'projects').document(PROJECT_ID).collection('guests').document(PROJECT_ID).collection('guest-data').stream()

for doc in guests:
    current = doc.to_dict()
    current['id'] = doc.id
    
    guest_reference.append(current)
    
PHONEBOOKAGENT = pd.DataFrame(guest_reference)


# ## Set up CHROMEDRIVER 

# In[ ]:


# Starting the selenium webserver and getting whatsapp 
userprofile = 'samarth'
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={cwd}/."+userprofile+"UserProfile")
driver = webdriver.Chrome(ChromeDriverManager().install() , options=options)
driver.get("https://web.whatsapp.com/")


# # 2.0 RUNTIME

# ## 2.1 Define automation functions

# In[ ]:




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
        
        attachSpecificElement = driverVar.find_elements(By.XPATH,f"//span[@data-testid='attach-document']")
        if len(attachSpecificElement)>0:
            print('[F_TOGGLE_CLIPPY_ON]-> Successfully, Opened Clippy')
            return 1
        else:
            print('[F_TOGGLE_CLIPPY_ON]->Error, in opening clippy, retrying','[try]: ',trial)
            F_TOGGLE_CLIPPY_ON(driverVar,trial = trial + 1)
            
            
            
        
    else:
        if trial < 5 :
            print('[F_TOGGLE_CLIPPY_ON]-> Error, No Clip Element Found on Page,Trying Again','[try]: ',trial)
            F_TOGGLE_CLIPPY_ON(driverVar,trial = trial + 1)
        else:
            return 0     

def F_GET_FILE(attachment_url):

    random.seed(datetime.now())
    file_name = str(random.random() * 100000).split('.')[0]
    if '.png' in attachment_url:
        file_format = 'png'
    elif '.pdf' in attachment_url:
        file_format = 'pdf'
    elif '.jpeg' in attachment_url:
        file_format = 'jpeg'
    elif '.jpg' in attachment_url:
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


    

def F_RECURSIVE_SEND_ATTACHMENT(driverVar,contact_number,attachment_address,trial_number=0):
    
    F_SEARCH_2(driverVar,contact_number)
    F_TOGGLE_CLIPPY_ON(driver)
    
    time.sleep(2)

    if '.pdf' in attachment_address:
        attachment_type = 'pdf'
    else:
        attachment_type = 'media'
        
    print(f'[F_RECURSIVE_SEND_ATTACHMENT]-> Attatchment type detected as : {attachment_type} ')


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
            
            attachInputElement[0].send_keys(attachment_address)
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
                F_RECURSIVE_SEND_ATTACHMENT(driverVar,contact_number,attachment_address,trial_number = trial_number+1)
    

    else:
        if trial_number>5:
                print('[F_RECURSIVE_SEND]-> Tries Exceeded 5, breaking')
                return 0
        else:
            print('[F_RECURSIVE_SEND]-> Cannot Find Attach-Specific Element(1), Rerunning After Toggle ')
            F_RESET_HARD(driverVar,RESET_NO)
            F_RECURSIVE_SEND_ATTACHMENT(driverVar,contact_number,attachment_address,trial_number = trial_number+1)


# ## 2.2 Infinite Running Loop (only Sending Messages)

# In[ ]:


while True:
    if FIREBASEAGENT.queue_length > 0 :
        for task in FIREBASEAGENT.queue:
#             print(task)
#             print('\n')
            TASKID = task['id']

            if task['type'] == 'send':
                if task['attachment'] == '':
                    PHONE = task['contactPhone']
                    MESSAGE = task['messageContent']
                    F_SEARCH_2(driver,PHONE)
                    F_SINGLE_SEND(driver,MESSAGE)
                    FIREBASEAGENT.server_update(TASKID,'done')

            elif task['type']=='sent':
                PHONE = task['contactPhone']
                URL = task['attachment']['url']
                F_RECURSIVE_SEND_ATTACHMENT(driver,PHONE,F_GET_FILE(URL))
                FIREBASEAGENT.server_update(TASKID,'done')


            else:
                pass

    time.sleep(10)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




