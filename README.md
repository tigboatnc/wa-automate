# Whatsapp Automation using Selenium 
- Only supports one user per instance, which is __hardcoded__ into the code. 
- Since whatsapp values contact syncing, I bypass that system by only using numbers. 

# BIG TODO 
- [ ] Sync Read and send messages (From Conversation and WAQUEUE)
- [ ] What happens on append ? ? ?? ? ? 
- [ ] Check if correct profile open in single send 
- [ ] Implement Batch Delete !!!! Very Very Important
- [ ] Ask shivam to change attachment type from __sent__  to __send type__ !!! im angry af .
- [ ] Remove TabRead Altogether (for now)
- [ ] Push to conversations  ******
- [ ] Startup causes first message to fail -> Add wait/ Check / timeout please
- [ ] Add user search into clippy 




## System Architecture 
### `CHROMEAGENT`
### `FIREBASEAGENT`
- Contains all tasks present in firebase which are pending. 
- Automatically gets new tasks in the variable. 
### `PHONEBOOKAGENT`




## Process Flow 
### 1. Setup 
1. Import libraries 
2. Set up FIREBASEAGENT 
3. Set up PHONEBOOKAGENT
3. Initialize CHROMEAGENT

## Functions 
### `F_GET_NEW_MSG`
- Uses `F_MESSAGE_READER` to get new_messages 
- Uses `F_PROFILE_VIEWER` to get profile 
> Gets new message on running this function in given format
```
    [
        {
            name : '<WhatsAppName>',
            number : '<WhatsAppNumber>',
            messageContent : [
                {

                }

            ]
        }

    ]
``` 

### `F_PROFILE_VIEWER` 
> For any given chat, opens the contact info and scrapes the name and title 

1. Only 2 headers on page and clicking one does nothing, clicking other opens contact info page so it clicks both. 

[ref](./ref_march_22/bubble.png)


