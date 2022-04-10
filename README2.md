# Full Restructure x2


Based on a status loop for providing more control over the entire process and circumvent the issue of multithreading.

## Core Idea
- __One process loop__ : One loop which includes all features and automation runs. 
- __No multithreading__ : Each runtime is an individual whatsapp server. The server gets commands periodically from firebase and implements them. <br/>
    `one issue this raises is sync issues if the software breaks but that can be corrected eventually`

## Structure 
- __PROCESS LOOP__<br/>
    - This loop runs infinitely
        - __Manage New Incoming Message__
            - Check and process any new messages (bubble processing)
            - Write to firestore 
        - __Manage Firebase Commands__
            - Get commands from firebase 
            - Run commands from firebase
            - Write to firestore 
            - Clear firebase commands 
        - Sleep for 5 seconds

- __FULLY FUNCTIONAL__<br/>
    - All functions are mostly self dependent, unless it is inefficient to do so.




## Goals
- [ ] Build Validation System
    - Check if the action actually completes
    - Add/Remove from firebase based on whether tasks are done or not
    <br/> _Plumbing already exists for each function as it returns a complete variable, just the necessary checks need to be added_ 


## Nomenclature
- __COMMAND_QUEUE__ : Commands from firebase 