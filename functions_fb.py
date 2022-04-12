from functions_utils import *

def FBASE_createNotification(db,CLIENT_ID,PROJECT_ID,notificationDoc):
    # --------------------------------------
    # Creates a notification for any {CLIENT_ID}, {PROJECT_ID}
    # Return : True if document created
    # Date : 04/01/2022
    # --------------------------------------
    
    doc_ref = db.collection(u'clients').document(CLIENT_ID).collection(u'projects').document(PROJECT_ID).collection('notification').add(notificationDoc)
    print(f'{str(reporting())} : Created a notification document at address { doc_ref[1].id}')
    return 1


def FBASE_getCommandQueue(db,CLIENT_ID,PROJECT_ID):
    # --------------------------------------
    # Gets the commands from wa-queue for any given {CLIENT_ID} and {PROJECT_ID}
    # Return : list(dict)
    # Date : 04/02/2022
    # --------------------------------------
    
    comQueue = []
    documents = db.collection(u'clients').document(CLIENT_ID).collection(u'projects').document(PROJECT_ID).collection('wa-queue').where(u'type', u'!=', 'tabread').stream()
    for doc in documents:
        cur_doc = doc.to_dict()
        cur_doc['DOCUMENT_ID'] = doc.id
        comQueue.append(cur_doc)
    if len(comQueue) > 0 :
        print(f'{str(reporting())} : Received new command queue with {len(comQueue)} commands')
        return comQueue
    else:
        return -1 

def FBASE_commandQueueVerification(CLIENT_ID,PROJECT_ID,COMMAND_QUEUE):
    # --------------------------------------
    #   1.Verify a COMMAND_QUEUE for missing phone number 
    ## TODO   2.Remove bad entries from firebase 
    #   3.Create Notification
    #   3.Return Correct Filtered List
    # Return : list(dict)
    # Date : 04/02/2022
    # --------------------------------------
    
    filtered_command_queue = []
    for command in COMMAND_QUEUE:
        guest_id = command['guestId']    
        command_id = command['DOCUMENT_ID']
        if 'contactPhone' not in command.keys():
            nMessage =  'Cannot find contact phone section'
            nType = 'wa_error_phone_notFound' # Server error 
            nHeader = f"Can't send message to {guest_id}"   
            print(f'{str(reporting())} : Dropped Command {command_id} due to wrong formatting : firebase error')
        elif command['contactPhone'] == '':
            print(f'{str(reporting())} : Dropped Command {command_id} due to wrong formatting : firebase error')
        else:   
            filtered_command_queue.append(command)
    return filtered_command_queue
 