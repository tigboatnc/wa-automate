# Firebase Imports 
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import threading

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

import time

today = date.today()
cwd = os.getcwd()


project_id = 'tpc-dev-5330f'
# Use the application default credentials
cred = firebase_admin.credentials.Certificate('./secret/tpc-dev-5330f-firebase-adminsdk-2p698-e13719db26.json')

firebase_admin.initialize_app(cred, {
  'projectId': project_id,
})

db = firestore.client()


doc_ref = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue')


# Create an Event for notifying main thread.
callback_done = threading.Event()
# MAIN VARIABLE : Clean after use 
process_queue = []

# Create a callback on_snapshot function to capture changes
def on_snapshot(col_snapshot, changes, read_time):
    for doc in col_snapshot:
#         print(f'{doc.id}')
        process_queue.append(doc.id)
    callback_done.set()
    

col_query = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').where(u'processed', u'==', False)

# Watch the collection query
query_watch = col_query.on_snapshot(on_snapshot)








# RUN WA AUTOMATION HERE --------------


# START WHATSAPP SEND 

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






while(True):
    
    
    print('Status - Sleep---------------')
    time.sleep(10)


    print('STATUS : Checking Queue')
    process_queue_clean = list(set(process_queue))


    if len(process_queue_clean)>0:  
        print(f'FOUND {len(process_queue_clean)} jobs')
    #     print(process_queue_clean)
        # -----------------
        
        print('STATUS : Running Job')
        for TASK_ID in process_queue_clean:
            task_doc_ref = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').document(TASK_ID)
            task_doc = task_doc_ref.get()
            TASKDATA = task_doc.to_dict()
#             print(TASKDATA)

            TASK_PHONE = TASKDATA['contactPhone']
            TASK_MESSAGE = TASKDATA['messageContent'] 
            TASKDATA['processed'] = True
            task_doc_ref = db.collection(u'clients').document(u'YIJ3bLzUXlubsxnDPnDR').collection(u'projects').document(u'BOuyALnDYmDHSBW7kAZm').collection('wa-queue').document(TASK_ID).set(TASKDATA)

            print('SEND TO : ', TASK_PHONE)
            print('MESSAGE : ',TASK_MESSAGE)


            F_SEARCH_2(driver,TASK_PHONE)
            F_SINGLE_SEND(driver,TASK_MESSAGE)
        process_queue = []
        


