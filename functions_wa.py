import time

from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from functions_utils import *
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import pandas as pd
from dateutil.parser import parse

def WA_messageTextParser(driver):
    # --------------------------------------
    # Get all messages on current open page 
    # Updated on : 04/09/2022, Reference : {040322_bubblediv.png}
    # Return : True
    # Date : 04/02/2022
    # --------------------------------------
    
    # Scrolling -------------------------------------
    
    chat_component = driver.find_elements(By.XPATH,f"//div[@role='region']")[0]
    time.sleep(2)
    driver.execute_script("arguments[0].scrollIntoView();", chat_component)
    time.sleep(2)


    CORPUS = [] 
    chat_component = driver.find_elements(By.XPATH,f"//div[@role='region']")[0]
    chat_children = chat_component.find_elements(By.XPATH,'.//*')
    for child in chat_children:
        if child.get_attribute('class'):
            attrlist = child.get_attribute('class').split(' ')
            if 'message-in' in attrlist:
                CORPUS.append({
                    'text':child.text,
                    'type':'mi'
                })
            elif 'message-out' in attrlist:
                CORPUS.append({
                    'text':child.text,
                    'type':'mo'
                })
            elif 'focusable-list-item' in attrlist:
                CORPUS.append({
                    'text':child.text,
                    'type':'fli'
                })


    PARSED_CORPUS = []
    TEMP_PUSH = []
    for division in CORPUS[::-1]:

        if division['type']=='mi':
            message = '\n'.join(division['text'].split('\n')[:len(division['text'].split('\n'))-1])
            timeSplit = division['text'].split('\n')[::-1][0]
            TEMP_PUSH.append({
                'time' : timeSplit,
                'msg':message,
                'type':'mi'})


        elif division['type']=='mo':
            message = '\n'.join(division['text'].split('\n')[:len(division['text'].split('\n'))-1])
            timeSplit = division['text'].split('\n')[::-1][0]
            TEMP_PUSH.append({
                'time' : timeSplit,
                'msg':message,
                'type':'mo'})

        elif division['type']=='fli':
            selected_date = -1
            if division['text'] == 'TODAY': # Check if today 
                selected_date = division['text']

            elif is_date(division['text']): # Check if date
                selected_date = division['text']


            if selected_date !=-1:
                for push in TEMP_PUSH:
                    push['date']=selected_date

                    PARSED_CORPUS.append(push)

                TEMP_PUSH = [] 



    return PARSED_CORPUS
    
def WA_PROFILE_VIEWER(driver):
    # --------------------------------------
    # Get the currently open profile 
    # Updated on : 04/11/2022
    # Return : True
    # Date : 04/02/2022
    # --------------------------------------
    
    # Scrolling -------------------------------------
    headers = driver.find_elements(By.XPATH,f"//header")
    for header in headers:
        header.click()
        time.sleep(1)

    headers = driver.find_elements(By.XPATH,f"//header")

    # validates if CF_PROFILE_VIEWERontact Info page is open is open 
    headerValidator = [] 
    for header in headers:
        headerValidator.append(header.text)

    if 'Contact info' in headerValidator:
        print('Yes we are in contact info page: Verified')
    else:
        print(str(reporting()),': Some error, maybe not in a user page')
        return 0
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


def WA_manageNewMessages(driver):
    # --------------------------------------
    # Manage New Messages Based on the bubble notifications.
    # Updated on : 04/03/2022, Reference : {040922_region.png}
    # Works on the basis that region is only one place in the document and contains all chat 
    # Then split based on message-in, message-out and focus
    # Return : True
    # Date : 04/02/2022
    # --------------------------------------
    
    
    
    BUBBLE_CLASS = '_1pJ9J'
    NEW_MESSAGES = []

    while True:
        bubbleList = driver.find_elements(By.XPATH,f"//div[@class='{BUBBLE_CLASS}']")
        if len(bubbleList) == 0 :
            break 
            
        print(f'{str(reporting())} : Found {len(bubbleList)} new messages, processing')
        bubbleList[0].click()
        
        # Getting current user details: 
        try:
            print(str(reporting()),': Checking user details  ')
            userNumber,userName = WA_PROFILE_VIEWER(driver)
        except Exception : 
            print(str(reporting()),': Issue in checking user details, skipping new message ')
            
        
        
        time.sleep(2)
        MESSAGE_BUNCH = {
            'no': userNumber,
            'name': userName,
            'messages' : WA_messageTextParser(driver)}
        
        NEW_MESSAGES.append(MESSAGE_BUNCH)
        time.sleep(2)
    
    return NEW_MESSAGES
    
    
    

def WA_SEARCH_2(driverVar,contact_number):
    # --------------------------------------
    # Search for a user on whatsapp
    # Returns 0 with error if not found 
    # Return : True
    # Date : 04/11/2022
    # --------------------------------------

    print(f'{str(reporting())}: ======== PROCESS STARTING : Parameter : {contact_number} ========')
    
    initial_search = WA_PROFILE_VIEWER(driverVar)

    driverVar.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.CONTROL + Keys.COMMAND + '//')
    time.sleep(1)


    FORM_HEADER_CLASS = '_1Jn3C' # Label Class
    FORM_CLASS = '_13NKt copyable-text selectable-text'

    formHeadingClassList = driverVar.find_elements(By.XPATH,f"//label[@class='{FORM_HEADER_CLASS}']")

#     print(len(formHeadingClassList))


    if len(formHeadingClassList)==1:
        formHeadingClass = formHeadingClassList[0]
        formElementsList = formHeadingClass.find_elements(By.XPATH,f".//div[@class='{FORM_CLASS}']")

#         print(len(formElementsList))

        if len(formElementsList)>0:
            formElement = formElementsList[0]
            formElement.click();
            formElement.clear();
            formElement.send_keys(f'{contact_number}')
            time.sleep(4)
            formElement.send_keys(Keys.RETURN)   
    
    # Checking if any user found 
    final_search = WA_PROFILE_VIEWER(driverVar)
    time.sleep(4)
    if initial_search == final_search :
        print(f'{str(reporting())}: User Not Found / search failed')
        return 0

def WA_SINGLE_SEND(driverVar,text_message):
    print(f'{str(reporting())}: ======== PROCESS STARTING : Parameter : {text_message} ========')
    CHAT_HEADER_CLASS = '_1UWac _1LbR4'
    ALT_CHAT_HEADER_CLASS = '_1UWac _1LbR4 focused'
    CHAT_CLASS = '_13NKt copyable-text selectable-text'

    print(f'{str(reporting)}: Trying Unfocussed')
    chatHeadingClassList = driverVar.find_elements(By.XPATH,f"//div[@class='{CHAT_HEADER_CLASS}']")
    if len(chatHeadingClassList)==0:
        print(f'{str(reporting)}: Unfocussed failed, trying focussed;')
        chatHeadingClassList = driverVar.find_elements(By.XPATH,f"//div[@class='{ALT_CHAT_HEADER_CLASS}']")
    print(f'{str(reporting)}: Length of Chat Header Div => {len(chatHeadingClassList)}')

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


def WA_parse_message_list(msg):
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    one_week_ago = today - timedelta(days=7)
    thirty_days_ago = today - timedelta(days=30)
    DATELIST = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']
    MSG_LIST = []
    for message in msg:
        DATE = message['date']
        CONTENT = message['msg']
        TIME = parse(message['time'])
        
        if DATE == 'TODAY':
            DATE_P = today
        elif DATE == 'YESTERDAY':
            DATE_P = today - timedelta(days=1)
        elif '/' in DATE:
            DATE_P = parse(DATE)
        else: 
            dateIndex = DATELIST.index(DATE)
            timeDelta = today.weekday() - dateIndex
            DATE_P = today - timedelta(days=timeDelta)
        
        hour = TIME.hour
        minute = TIME.minute
        DATE_P = DATE_P.replace(hour=hour, minute=minute,second = 0)
        
        
        MSG_LIST.append ({
            'TIMESTAMP' : DATE_P,
            'CONTENT' : CONTENT,
            'TYPE' : message['type'],
            
        })
        
        df = pd.DataFrame(MSG_LIST)
        return df


def WA_OpenGallery2(driver,trialNumber,found):
    # Very messy function 
    
    head_component = driver.find_elements(By.XPATH,f"//div[@id='app']")[0]
    modal_component = head_component.find_elements(By.XPATH,f".//div[@data-testid='media-viewer-modal']")

    if len(modal_component) == 1:
        print('Found Modal')
        found = 1 
        return True
    trialNumber = trialNumber + 1 

    if trialNumber>5:
        print('Cannot find gallery hook')
        return False
    else:
        print(f'Open Gallery, Trial : {trialNumber}')

    time.sleep(2)
    chat_component = driver.find_elements(By.XPATH,f"//div[@role='region']")[0]
    img_dl = chat_component.find_elements(By.XPATH,".//div[@data-testid='media-state-download']")
    img_dld = chat_component.find_elements(By.XPATH,".//div[@data-testid='media-url-provider']")

    if len(img_dl) + len(img_dld) == 0:
        chat_component = driver.find_elements(By.XPATH,f"//div[@role='region']")[0]
        driver.execute_script("arguments[0].scrollIntoView();", chat_component)
        time.sleep(1)
        WA_OpenGallery2(driver,trialNumber+1,0)

    for element in img_dl + img_dld:
        try:
            element.click()
            head_component = driver.find_elements(By.XPATH,f"//div[@id='app']")[0]
            time.sleep(2)
            modal_component = head_component.find_elements(By.XPATH,f".//div[@data-testid='media-viewer-modal']")

            if len(modal_component) == 1:
                print('Found Modal')
                found = 1 
                return True
            else:
                continue

        except Exception:
            print('Tried Clicking, error')

    if found == 0 :
        WA_OpenGallery2(driver,trialNumber+1,0)
        