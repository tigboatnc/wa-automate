#!/usr/bin/env python
# coding: utf-8

# `/clients/YIJ3bLzUXlubsxnDPnDR/projects/BOuyALnDYmDHSBW7kAZm/wa-queue`|

# In[1]:


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
import re

import time

today = date.today()
cwd = os.getcwd()


# In[2]:


project_id = 'tpc-dev-5330f'
# Use the application default credentials
cred = firebase_admin.credentials.Certificate('./secret/tpc-dev-5330f-firebase-adminsdk-2p698-e13719db26.json')

firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()


# In[3]:


# Create an Event for notifying main thread.
callback_done = threading.Event()
callback_done = threading.Event()
# MAIN VARIABLE : Clean after use 
process_queue_send = []
process_queue_tabread = []

# Create a callback on_snapshot function to capture changes
def waQueueSendSnapshot(col_snapshot, changes, read_time):
    for doc in col_snapshot:
        process_queue_send.append(doc.id)
    callback_done.set()
    
def waQueueTabReadSnapshot(col_snapshot, changes, read_time):
    for doc in col_snapshot:
        process_queue_tabread.append(doc.id)
    callback_done.set()

send_query = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').where(u'processed', u'==', False).where(u'type', u'==', 'send')
tabread_query = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').where(u'processed', u'==', False).where(u'type', u'==', 'tabread')


# Watch the collection query
send_query_watch = send_query.on_snapshot(waQueueSendSnapshot)
tab_read_watch = tabread_query.on_snapshot(waQueueTabReadSnapshot)


# In[ ]:


# Starting the selenium webserver and getting whatsapp 
userprofile = 'samarth'
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={cwd}/."+userprofile+"UserProfile")
driver = webdriver.Chrome(ChromeDriverManager().install() , options=options)
driver.get("https://web.whatsapp.com/")


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
            

def GET_CURRENT_CHATS(driverVar):

    CHATS_HEADER_CLASS = '_3K4-L' # 'y8WcF'
    chatHeadingClassList = driverVar.find_elements(By.XPATH,f"//div[@class='{CHATS_HEADER_CLASS}']")

    text_blob = chatHeadingClassList[0].text

    text_blob_list = chatHeadingClassList[0].find_elements(By.XPATH,"./*")

    MESSAGE_LIST= []

    from datetime import datetime

    datetime_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')



    def checkTimeBlob(line):
        timeREG = re.compile('^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$')
        return bool(timeREG.match(line))


    def checkDateBlob(line):
        dateREG = re.compile('^([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)\d{4}$')
        return bool(dateREG.match(line))

    current_date = ''

    for element in text_blob_list:
        element_class = element.get_attribute('class')
        element_text = element.text

    #     print(element_class)
    #     print(element_text)


        # Checking for date 
        if 'message' not in element_class and checkDateBlob(element_text) :
            current_date = element_text
    
        elif 'message' not in element_class and not checkDateBlob(element_text) and element_text=='TODAY':
            day_ref = datetime.now()
            current_date = '{:02d}'.format(day_ref.day) +'/' + '{:02d}'.format(day_ref.month) +'/'+ '{:02d}'.format(day_ref.year)
        
        elif 'message' not in element_class and not checkDateBlob(element_text) and element_text=='YESTERDAY':
            day_ref = datetime.now() - timedelta(days = 1)
            current_date = '{:02d}'.format(day_ref.day) +'/' + '{:02d}'.format(day_ref.month) +'/'+ '{:02d}'.format(day_ref.year)

        elif 'message-in' in element_class:
            if current_date == '':
                print('Date Parsing Error')
                break

            message_in_time = element_text.split('\n')[::-1][0]
            message_in_time_full = message_in_time + ' ' + current_date
            message_in_time_full_parse = datetime.strptime(message_in_time_full, '%H:%M %m/%d/%Y')
            message_in_text = '\n'.join(element_text.split('\n')[:len(element_text.split('\n'))-1])

            MESSAGE_LIST.append(
            {
                'type': 'in',
                'time': message_in_time_full_parse,
                'content':message_in_text
            })

        elif 'message-out' in element_class:
            if current_date == '':
                print('Date Parsing Error')
                break

            message_out_time = element_text.split('\n')[::-1][0]
            message_out_time_full = message_out_time + ' ' + current_date
            message_out_time_full_parse = datetime.strptime(message_out_time_full, '%H:%M %d/%m/%Y')
            message_out_text = '\n'.join(element_text.split('\n')[:len(element_text.split('\n'))-1])

            MESSAGE_LIST.append(
            {
                'type': 'in',
                'time': message_out_time_full_parse,
                'content':message_out_text
            })
    return MESSAGE_LIST



# In[ ]:


while True:
    
    print('\n\n SLEEPING')
    time.sleep(10)
    
#     -----------------------------------------------------------------------------------------------------------------------

    print('\n\n SEND - QUEUE - PROCESSING')

    # 1.  -------------------------- Get current task list --------------------------
    process_queue_clean = list(set(process_queue_send))

    # All the tasks to be carried out 
    TASKLIST = []
    print(f'Found {len(process_queue_clean)} tasks')
    for task_id in process_queue_clean:
        task_doc_ref = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').document(task_id)
        task_doc = task_doc_ref.get()
        TASKDATA = task_doc.to_dict()
        if TASKDATA:

            TASKDATA['task_id'] = task_id
            TASKLIST.append(TASKDATA)

    # 1.1 -------------------------- Pre-Process the task list --------------------------
    # Add python readable date to the task list 
    for task in TASKLIST:
        task['pythonDate'] = datetime.fromtimestamp(task['createdAt'].timestamp())

    # Sorting list based on which message is supposed to be sent earlier 
    TASKLIST.sort(key=lambda item:item['createdAt'])

    # 2. -------------------------- Process task list --------------------------

    for task in TASKLIST:


        message_target = task['contactPhone']
        message_content = task['messageContent']

        print('Running Task : SEND')
        print(f'Sending Message to : {message_target}')
        print(f'Message Content : {message_content}')


    #   TODO : Add verification for sent text 

        F_SEARCH_2(driver,message_target)
        F_SINGLE_SEND(driver,message_content)

        task['completedAt'] = datetime.now()
        task['status'] = 'completed'

        print('\n')


    # 3. -------------------------- Post Processing --------------------------
    for task in TASKLIST:

        TASK_ID = task['task_id']
        GUEST_ID = task['guestId']

        MESSAGE_CONTENT = task['messageContent']
        timestamp_completed = task['completedAt']
        timestamp_created = task['pythonDate']




        if task['status'] == 'completed':
            # Removing the task from wa-queue 

            db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').document(TASK_ID).delete()



            # Adding conversation to the guest collection
            MESSAGE_DOCUMENT = {
                'message' : MESSAGE_CONTENT,
                'completedAt' : timestamp_completed,
                'createdAt' : timestamp_created,
                'context' : 'wa-send',
                'type' : 'sent',
                'attachment': ''
            }
            db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('guests').document(u'BOuyALnDYmDHSBW7kAZm').collection(u'guest-data').document(GUEST_ID).collection(u'conversations').add(MESSAGE_DOCUMENT)


        # Cleaning up process queue
        process_queue_send = []

#     -----------------------------------------------------------------------------------------------------------------------
        
    print('\n\n TABREAD - QUEUE - PROCESSING')



    process_queue_clean = list(set(process_queue_tabread))

    # 1.  -------------------------- Get current task list --------------------------

    # All the tasks to be carried out 
    TASKLIST = []
    print(f'Found {len(process_queue_clean)} tasks')
    for task_id in process_queue_clean:
        task_doc_ref = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').document(task_id)
        task_doc = task_doc_ref.get()
        TASKDATA = task_doc.to_dict()
        if TASKDATA:

            TASKDATA['task_id'] = task_id
            TASKLIST.append(TASKDATA)


    # 1.1 -------------------------- Pre-Process the task list --------------------------
    # Add python readable date to the task list 
    for task in TASKLIST:
        task['pythonDate'] = datetime.fromtimestamp(task['createdAt'].timestamp())

    # Sorting list based on which message is supposed to be sent earlier 
    TASKLIST.sort(key=lambda item:item['createdAt'])


    # 2. -------------------------- Process task list --------------------------

    for task in TASKLIST:


        message_target = task['contactPhone']
        GUEST_ID = task['guestId']


        print('Running Task : TABREAD')



        F_SEARCH_2(driver,message_target)
        CURRENT_USER_CHATS = GET_CURRENT_CHATS(driver)
        print(CURRENT_USER_CHATS)


        task['completedAt'] = datetime.now()
        task['status'] = 'completed'

        for messages_to_push in CURRENT_USER_CHATS:

            if messages_to_push['type']== 'in':
                message_type = 'recieved'
            elif messages_to_push['type']== 'out':
                message_type = 'sent'

            MESSAGE_DOCUMENT = {
                    'message' : messages_to_push['content'],
                    'completedAt' : messages_to_push['time'],
                    'createdAt' : task['completedAt'],
                    'context' : 'tabread',
                    'type' : message_type,
                    'attachment': ''
                }
            db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('guests').document(u'BOuyALnDYmDHSBW7kAZm').collection(u'guest-data').document(GUEST_ID).collection(u'conversations').add(MESSAGE_DOCUMENT)

        print('\n')
    process_queue_tabread = []


    
        
        


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




