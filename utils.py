########################
########################
###                  ###
###     IMPORTS      ###
###                  ###
########################
########################

try:
    from datetime import datetime
    import os
    import platform
    import time
    from threading import Timer
except:
    print("ERROR LOADING PYTHON: utils.py")

try:
    import RPi.GPIO as GPIO
except:
    print("ERROR LOADING GPIO: utils.py")

try:
    from config import ALARM_MINUTE, ALARM_HOUR, ALARM_SET
except:
    print("ERROR LOADING CONFIG: utils.py")

VERSION = 0.4
AUTHOR = "David Miles"

########################
########################
###                  ###
###    GPIO SETUP    ###
###                  ###
########################
########################

LED_PIN = 27
RELAY_PIN = 21
SET_BUTTON_PIN = 13
ALARM_BUTTON_PIN = 26
HOUR_BUTTON_PIN = 5
MINUTE_BUTTON_PIN = 6

def setup_pins():
    # Board Mode BCM
    GPIO.setmode(GPIO.BCM)

    # Disable Warnings
    GPIO.setwarnings(False)

    # Hour button
    GPIO.setup(HOUR_BUTTON_PIN, GPIO.IN)

    # Minute button
    GPIO.setup(MINUTE_BUTTON_PIN, GPIO.IN)

    # Set Alarm Button
    GPIO.setup(SET_BUTTON_PIN, GPIO.IN)

    # Alarm ON/OFF Button
    GPIO.setup(ALARM_BUTTON_PIN, GPIO.IN)

    # LED
    GPIO.setup(LED_PIN, GPIO.OUT)
    GPIO.output(LED_PIN, GPIO.LOW)

    # Relay
    GPIO.setup(RELAY_PIN, GPIO.OUT)
    GPIO.output(RELAY_PIN, GPIO.LOW)


#############################
#############################
###                       ###
###  MAIN CLOCK FUNCTION  ###
###                       ###
#############################
#############################

RECENTLY_SOUNDED = False

def run_clock(os_name, loop_bool):
    ALARM_SOUNDING = False

    try:
        while True:
            display_welcome(os_name, loop_bool)

            current_time = get_current_time()
            
            print(f"The current time is: {current_time}")

            print_debug_output(current_time)


            # Check to see if set alarm button is pressed
            if GPIO.input(SET_BUTTON_PIN) == False:
                print("Set Button Held")

                # Add an hour when the button is pressed
                if GPIO.input(HOUR_BUTTON_PIN) == False:
                    print("hour")
                    global ALARM_HOUR
                    ALARM_HOUR = ALARM_HOUR + 1
                    if ALARM_HOUR == 24:
                        ALARM_HOUR = 0
                    sleep(0.2)
                
                # Add a minute when the button is pressed
                if GPIO.input(MINUTE_BUTTON_PIN) == False:
                    print("minute")
                    global ALARM_MINUTE
                    ALARM_MINUTE = ALARM_MINUTE + 1
                    if ALARM_MINUTE == 60:
                        ALARM_MINUTE = 0
                    sleep(0.2)

            # Turn alarm on/off when button is pressed
            if GPIO.input(ALARM_BUTTON_PIN) == False:
                global ALARM_SET
                ALARM_SET = not ALARM_SET
                sleep(0.2)

            # Check to see if alarm needs to sound
            if ALARM_SET == True and RECENTLY_SOUNDED == False:
                if current_time.hour == ALARM_HOUR and current_time.minute == ALARM_MINUTE:
                    if GPIO.input(SET_BUTTON_PIN):
                        ALARM_SOUNDING = True

                        # Output to console
                        print("ALARM!!!")

                        # Turn on LED
                        GPIO.output(LED_PIN, GPIO.HIGH)

                        # Turn on Relay
                        GPIO.output(RELAY_PIN, GPIO.HIGH)
                else:
                    ALARM_SOUNDING = False
                    GPIO.output(LED_PIN, GPIO.LOW)
                    GPIO.output(RELAY_PIN, GPIO.LOW)
            else:
                ALARM_SOUNDING = False
                GPIO.output(LED_PIN, GPIO.LOW)
                GPIO.output(RELAY_PIN, GPIO.LOW)

            # Activate Pump if alarm is sounding
            if ALARM_SOUNDING == True:
                sleep(3)
                GPIO.output(LED_PIN, GPIO.LOW)
                GPIO.output(RELAY_PIN, GPIO.LOW)
                set_recently_sounded()
                #global RECENTLY_SOUNDED
                #RECENTLY_SOUNDED = True
                Timer(60, set_recently_sounded).start()

            sleep(0.05)
    except KeyboardInterrupt:
        clear


########################
########################
###                  ###
###   Alarm Tools    ###
###                  ###
########################
########################

def create_alarm_string(hour, minute):

    if hour < 10:
        hour_string = "0" + str(hour)
    elif hour == 24:
        hour_string = "00"
    else:
        hour_string = str(hour)

    if minute < 10:
        minute_string = "0" + str(minute)
    elif minute == 60:
        minute_string = "00"
    else:
        minute_string = str(minute)

    alarm_string = hour_string + ":" + minute_string

    return alarm_string


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


def print_debug_output(time_stamp):
    ALARM_TIME = create_alarm_string(ALARM_HOUR, ALARM_MINUTE)

    if ALARM_SET == True:
         alarm_to_display = f"Line 2:   |ALARM:ON {ALARM_TIME}xx|"
    else:
         alarm_to_display = "Line 2:   |ALARM: OFF      |"
    time_to_display = time_stamp.strftime("%H:%Mxx %m/%d/%y")
   
    
    print("\n\n##### SCREEN OUTPUT #####\n")
    print("Position:  0123456789012345")
    print("          ------------------")
    print(f"Line 1:   |{time_to_display}|")
    print(alarm_to_display)
    print("          ------------------")

def set_recently_sounded():
    global RECENTLY_SOUNDED
    RECENTLY_SOUNDED = not RECENTLY_SOUNDED


########################
########################
###                  ###
###  Generic Tools   ###
###                  ###
########################
########################

def sleep(num):
    time.sleep(num)

def clear():
    os_info = get_os_info()

    msg = os_info["message"]

    os.system(msg)


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


'''
def convert_am_pm(the_time):
    if the_time.hour > 12:
        new_hour = the_time.hour - 12
'''

########################
########################
###                  ###
###  Error Handling  ###
###                  ###
########################
########################

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