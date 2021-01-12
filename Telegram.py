from telethon.tl.types import UserStatusOnline, UserStatusRecently, UserStatusOffline
from telethon.tl.functions.users import GetFullUserRequest
from telethon.sync import TelegramClient
from telethon import events
from datetime import datetime
import time
import os.path
import os

# Connecting To Telegram
target = input("Enter target's contact name / username starting with '@' ")
phone = input("Enter you'r phone number starting with '+' ")
api_id = input("Enter you'r API ID ")
api_hash = input("Enter you'r API Hash ")
client = TelegramClient(phone, api_id, api_hash)
client.start()

if client.is_user_authorized():
    print(f"Session started at : {datetime.now()}")
    time.sleep(2)
    user = client.get_me()
    users_name = user.username
    print(f"Hello {users_name} ! Welcome to Telegram ;)")
    time.sleep(2)
else:
    client.send_code_request(phone)
    client.sign_in(phone, input('Please enter the code given by Telegram : '))


# If old log files detected separate / delete
old_key = True
while old_key:
    if os.path.isfile(f'{target}.txt') or os.path.isfile(f'{target}_log.txt') or os.path.isfile('randoms_log.txt'):
        old_files = input("Old logs files were found... \nType Yes to create new log files or No in order to use old files. ")
        if old_files == "Yes" or old_files == "yes" or old_files == "YES":
            print("Deleting old log files.")
            if os.path.isfile(f'{target}.txt'):
                os.remove(f'{target}.txt')
            if os.path.isfile(f'{target}_log.txt'):
                os.remove(f'{target}_log.txt')
            if os.path.isfile('randoms_log.txt'):
                os.remove('randoms_log.txt')
            old_key = False
        elif old_files == "No" or old_files == "no" or old_files == "NO":
            print("Separating old logs files with '###' line.")
            if os.path.isfile(f'{target}.txt'):
                target_full = open(f'{target}.txt', "a")
                print("###################################### \n", file=target_full)
                target_full.close()
            if os.path.isfile(f'{target}_log.txt'):
                target_file = open(f'{target}_log.txt', "a")
                print("###################################### \n", file=target_file)
                target_file.close()
            if os.path.isfile('randoms_log.txt'):
                rnd_log = open('randoms_log.txt', "a")
                print("###################################### \n", file=rnd_log)
                rnd_log.close()
            old_key = False
        elif old_files == "done" or old_files == "DONE" or old_files == "Done":
            print("Good bye.")
            quit
        else:
            print("Incorrect syntax. Please type 'Yes/No' or 'Done' to leave.")
    else:
        old_key = False

# Creating files with certian outputs
target_details = client(GetFullUserRequest(target))
td = target_details
target_id = client.get_peer_id(target)
first_msg = False
time.sleep(2)
print(f"Started listening to {target}. \n{target}.txt created with basic user information.")
if td.user.id != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"{target}'s ID : " + str(td.user.id), "\n", file=target_full)
    target_full.close()
if td.user.verified != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"Does {target} verified ? " + str(td.user.verified),"\n",file=target_full)
    target_full.close()
if td.user.access_hash != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"{target}'s access hash is : " + str(td.user.access_hash),"\n",file=target_full)
    target_full.close()
if td.user.first_name != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"{target}'s first name is : " + str(td.user.first_name),"\n",file=target_full)
    target_full.close()
if td.user.username != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"{target}'s username is : " + str(td.user.username),"\n", file=target_full)
    target_full.close()
if td.user.last_name != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"{target}'s last name is : " + str(td.user.last_name),"\n",file=target_full)
    target_full.close()
if td.user.phone != 'None':
    target_full = open(f"{target}.txt", "a")
    print(f"{target}'s phone number is : " + str(td.user.phone),"\n", file=target_full)
    target_full.close()
time.sleep(2)

print(f"Creating {target}_log.txt as target's log file.")
time.sleep(2)
print(f"{target}'s User ID is : {target_id}")
target_file = open(f"{target}_log.txt", "a")
print(f"Session started by {users_name} at : {datetime.now()} \n",file=target_file)
print(f"{target}'s User ID is : {target_id} \n", file=target_file)
target_file.close()
time.sleep(2)


# Checking if the target is online when the script first run
async def first_con():
    global first_msg
    target_entity = await client.get_entity(target)
    if isinstance(target_entity.status, UserStatusOnline):
        print(f"{target} is correctly Online. \n")
        target_file = open(f"{target}_log.txt", "a")
        print(f"{target} Was Online at {datetime.now()} \n", file=target_file)
        target_file.close()
        first_msg = True
    if isinstance(target_entity.status, UserStatusOffline) or isinstance(target_entity.status, UserStatusRecently):
        print(f"{target} is correctly Offline. \n")
        time.sleep(2)
        target_file = open(f"{target}_log.txt", "a")
        print(f"{target} was Offline at {datetime.now()} \n", file=target_file)
        target_file.close()
        first_msg = True


# Save events on two logs, target_log and randoms_log
@client.on(events.UserUpdate())
async def handler(event):
    target_entity = await client.get_entity(target)
    global first_msg
    if first_msg == False:
        await first_con()
        print("Handler Log : \n")
    target_event = await client.get_entity(event.user_id)
    if target_event.first_name == target_entity.username:
        if event.status:
            print(f"{datetime.now()} : {target} came Online...")
            target_file = open(f"{target}_log.txt", "a")
            print(f"{target} went Online at : {datetime.now()} \n",file=target_file)
            target_file.close()
        if event.typing:
            print(f"{datetime.now()} : {target} is typing...")
            target_file = open(f"{target}_log.txt", "a")
            print(f"{target} typed a message at : {datetime.now()} \n", file=target_file)
            target_file.close()
        if event.recently:
            print(f"{datetime.now()} : {target} went Offline...")
            target_file = open(f"{target}_log.txt", "a")
            print(f"{target} went Offline at : {datetime.now()} \n",file=target_file)
            target_file.close()
    else:
        event_details = await client.get_entity(event.user_id)
        event_username = event_details.username
        event_name = event_details.first_name
        print(f"Event from {event_name} was saved on randoms_log.txt")
        rnd_log = open(f'randoms_log.txt', 'a')
        print(f"Event from {event_username} as {event_name} at {datetime.now()}.",file=rnd_log)
        print(event.status, "\n", file=rnd_log)
        rnd_log.close()
client.run_until_disconnected()
