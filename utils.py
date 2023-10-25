from datetime import datetime
import os
import platform
import time

try:
    from config import ALARM_TIME, ALARM_SET
except:
    print("ERROR LOADING CONFIG")

VERSION = 0.1
AUTHOR = "David Miles"

def clear():
    os_info = get_os_info()

    msg = os_info["message"]

    os.system(msg)


def display_welcome(os_name, loop_bool):
    clear()
    print(f"System is running: {os_name}")
    print("***************************************")
    print("*    /\    |       /\    |``\  |\  /| *")
    print("*   /__\   |      /__\   |__|  | \/ | *")
    print("*  /    \  |     /    \  | \   |    | *")
    print("* /      \ |___ /      \ |  \  |    | *")
    print("*                                     *")
    print("*      /```  |    /``\   /``` | /     *")
    print("*     |      |   |    | |     |/      *")
    print("*     |      |   |    | |     |\      *")
    print("*      \___  |___ \__/   \___ | \     *")
    print("***************************************")
    print(f"Version: {VERSION}")
    print(f"Author: {AUTHOR}\n\n")

    if loop_bool == True:
        print("************************")
        print("* PRESS CTRL+C TO EXIT *")
        print("************************")
        print("\n")


def get_current_time():
    current_time = datetime.now()
    return current_time


def get_os_info():
    OS_platform = platform.system()

    clear_message = ""
    name = ""

    if OS_platform == "Windows":
        clear_message = "cls"
        name = "Windows"
    elif OS_platform == "Linux":
        clear_message = "clear"
        name = "Linux"
    elif OS_platform == "Darwin":
        clear_message = "clear"
        name = "MacOS"
    else:
        print_error(OS_ERROR)
    
    return {"name": name, "message": clear_message}

def print_debug_output(time_stamp):
    time_to_display = time_stamp.strftime("%H:%M %m/%d/%Y")
    
    print("0123456789012345")
    print(time_to_display)
    if ALARM_SET == True:
        print(f"ALARM: ON {ALARM_TIME}")



def run_clock(os_name, loop_bool):
    try:
        while True:
            display_welcome(os_name, loop_bool)

            current_time = get_current_time()
            
            print(f"The current time is: {current_time}")

            print_debug_output(current_time)
            
            sleep(0.2)
    except KeyboardInterrupt:
        clear


def sleep(num):
    time.sleep(num)


'''
def convert_am_pm(the_time):
    if the_time.hour > 12:
        new_hour = the_time.hour - 12
'''

#   ####################
#   ## ERROR HANDLING ##
#   ####################

DEFAULT_ERROR = "An unexpected error occured. Fuck."
EXIT_MESSAGE = "Thank you for using!"
OS_ERROR = "ERROR:\nOS not supported.\nCurrently supported operating systems:\n\t*Windos\n\t*MacOS\n\t*Linux"

def print_error(err, msg1="", msg2=""):
    clear()
    print("\n")
    print("**********************************************************************")
    print("\n")
    print(err)
    print("\n")
    print("**********************************************************************")

    if msg1 != "":
        print(f"{msg1}\n")
    if msg2 != "":
        print(f"{msg2}\n")
    
    print("\n")
    print("Press ENTER to exit...")
    input("")
    clear()
    exit()