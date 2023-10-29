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
    from config import \
        ALARM_MINUTE,\
        ALARM_HOUR,\
        ALARM_SET,\
        ALARM_DURATION,\
        DELAY_TIME
except:
    print("ERROR LOADING CONFIG: utils.py")

try:
    from lcd import lcd_init,\
        lcd_text,\
        LCD_E,\
        LCD_RS,\
        LCD_D4,\
        LCD_D5,\
        LCD_D6,\
        LCD_D7,\
        LCD_LINE_1,\
        LCD_LINE_2
except:
    print("ERROR LOADING LCD RESOURCES: utils.py")

VERSION = 0.6
AUTHOR = "David Miles"

########################
########################
###                  ###
###    GPIO SETUP    ###
###                  ###
########################
########################

# Conponent Pins
LED_PIN = 27
RELAY_PIN = 21
SET_BUTTON_PIN = 13
ALARM_BUTTON_PIN = 26
HOUR_BUTTON_PIN = 5
MINUTE_BUTTON_PIN = 6

# Set up pins for all components
def setup_pins():
    # Board Mode: BCM
    GPIO.setmode(GPIO.BCM)

    # Disable Warnings
    GPIO.setwarnings(False)

    # LCD Pins
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_D4, GPIO.OUT)
    GPIO.setup(LCD_D5, GPIO.OUT)
    GPIO.setup(LCD_D6, GPIO.OUT)
    GPIO.setup(LCD_D7, GPIO.OUT)

    # Initialize LCD screen
    lcd_init()

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

# This variable becomes true when the alarm sounds, 
# and remains true for 60 seconds. This prevents the
# alarm from sounding again during the same minute.
RECENTLY_SOUNDED = False
SNOOZING = False

def run_clock(os_name, loop_bool):

    try:
        while True:
            display_welcome(os_name, loop_bool)

            current_time = get_current_time()
            
            print(f"The current time is: {current_time}")

            check_button_press()

            print_debug_button_output()

            print_clock_output(current_time)

            check_sound_alarm(current_time)

            sleep(0.05)
    except KeyboardInterrupt:
        clear
        lcd_init()


########################
########################
###                  ###
###   Alarm Tools    ###
###                  ###
########################
########################


# Check if the 'set' button is being pressed.
def check_button_press():
    

    if (GPIO.input(HOUR_BUTTON_PIN) == False and GPIO.input(MINUTE_BUTTON_PIN) == False) and GPIO.input(SET_BUTTON_PIN):

        # Turn on LED
        GPIO.output(LED_PIN, GPIO.HIGH)

        # Turn on Relay
        GPIO.output(RELAY_PIN, GPIO.HIGH)

        # Run pump for 1 second
        sleep(1)

        # Turn off pump and LED pins
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(RELAY_PIN, GPIO.LOW)

        # Give the circuit time to recover before initializing screen.
        sleep(0.1)

        # Re-initialize screen to deal with any voltage spike interference.
        lcd_init()


    # Check to see if 'set alarm' button is pressed
    if GPIO.input(SET_BUTTON_PIN) == False:
        global SNOOZING
        SNOOZING = False

        # Add an hour when the button is pressed
        if GPIO.input(HOUR_BUTTON_PIN) == False:
            global ALARM_HOUR
            ALARM_HOUR = ALARM_HOUR + 1
            if ALARM_HOUR == 24:
                ALARM_HOUR = 0
            sleep(0.05)
        
        # Add a minute when the button is pressed
        if GPIO.input(MINUTE_BUTTON_PIN) == False:
            global ALARM_MINUTE
            ALARM_MINUTE = ALARM_MINUTE + 1
            if ALARM_MINUTE == 60:
                ALARM_MINUTE = 0

    # Turn alarm on/off when button is pressed
    if GPIO.input(ALARM_BUTTON_PIN) == False:
        global ALARM_SET
        ALARM_SET = not ALARM_SET
        sleep(0.2)


# Check to see if alarm needs to sound.
def check_sound_alarm(current_time):

    # This variable is set to True when
    # the pump needs to be activated.
    ALARM_SOUNDING = False

    global RECENTLY_SOUNDED
    global SNOOZING

    if ALARM_SET == True and RECENTLY_SOUNDED == False:
        if current_time.hour == ALARM_HOUR and current_time.minute == ALARM_MINUTE:
            if GPIO.input(SET_BUTTON_PIN):
                ALARM_SOUNDING = True

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
        # Clear screen and display "wake up" message
        lcd_init()
        lcd_text("    WAKE UP!    ", LCD_LINE_1)

        # Run pump for time specified in config.py
        sleep(ALARM_DURATION)

        # Turn off pump and LED pins
        GPIO.output(LED_PIN, GPIO.LOW)
        GPIO.output(RELAY_PIN, GPIO.LOW)

        SNOOZING = True

        # print("snoozeing set to true")
        # sleep(2)
        
        snooze_timer = Timer(DELAY_TIME, snooze_check)
        snooze_timer.start()

        # Set recently_sounded to True
        RECENTLY_SOUNDED = True

        # Start timer to prevent pump from activating again immediately.
        recently_sounded_timer = Timer(60, set_recently_sounded)
        recently_sounded_timer.start()



        # print("timer set")
        # print(snooze_timer)
        # sleep(2)




        # Give the circuit time to recover before initializing screen.
        sleep(0.1)

        # Re-initialize screen to deal with any voltage spike interference.
        lcd_init()


# Build the string that will be displayed
# on the second line of the LCD screen.
def create_alarm_string(hour, minute):
    am_pm = "AM"

    if hour == 0:
        hour_string = "12"
    elif hour == 12:
        hour_string = str(hour)
        am_pm = "PM"
    elif hour < 10:
        hour_string = " " + str(hour)
    elif hour < 12:
        hour_string = str(hour)
    elif hour > 12 and hour < 22:
        hour = hour - 12
        hour_string = " " + str(hour)
        am_pm = "PM"
    else:
        hour = hour - 12
        hour_string = str(hour)
        am_pm = "PM"

    if minute < 10:
        minute_string = "0" + str(minute)
    else:
        minute_string = str(minute)

    alarm_string = hour_string + ":" + minute_string + am_pm

    return alarm_string

IS_TURNING_ON = True

# Welcome message for console.
def display_welcome(os_name, loop_bool):
    global IS_TURNING_ON

    global SNOOZING
    global RECENTLY_SOUNDED

    clear()

    print(f"SNOOZING: {SNOOZING}")
    print(f"RECENT: {RECENTLY_SOUNDED}")


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
    
    if IS_TURNING_ON == True:
        display_welcome_lcd()
        IS_TURNING_ON = False



# Output to console and LCD screen
def print_clock_output(time_stamp):
    ALARM_TIME = create_alarm_string(ALARM_HOUR, ALARM_MINUTE)

    if ALARM_SET == True and GPIO.input(SET_BUTTON_PIN) == False:
        alarm_to_display = f"ALARM:ON {ALARM_TIME}"
    elif ALARM_SET == True:
         alarm_to_display = f"ALARM:ON        "
    else:
         alarm_to_display = "ALARM: OFF      "
    time_to_display = time_stamp.strftime("%I:%M%p %a%m/%d")

    if time_to_display[0] == "0":
        time_list = list(time_to_display)
        time_list[0] = ""
        time_to_display = ''.join(time_list)
        time_to_display = time_to_display[:10] + " " + time_to_display[10:]
    
    print("\n\n##### SCREEN OUTPUT #####\n")
    print("Position:  0123456789012345")
    print("          ------------------")
    print(f"Line 1:   |{time_to_display}|")
    print(f"Line 2:   |{alarm_to_display}|")
    print("          ------------------")

    lcd_text(time_to_display, LCD_LINE_1)
    lcd_text(alarm_to_display, LCD_LINE_2)


# Toggles the RECENTLY_SOUNDED variable
def set_recently_sounded():
    global RECENTLY_SOUNDED
    RECENTLY_SOUNDED = False

def snooze_check():
    global SNOOZING
    global RECENTLY_SOUNDED
    
    if SNOOZING == True:
        RECENTLY_SOUNDED = False
    else:
        SNOOZING = False


def display_welcome_lcd():
    lcd_text("*   Welcome    *", LCD_LINE_1)
    lcd_text("--Water Alarm-- ", LCD_LINE_2)

    print("*   Welcome    *")
    print("--Water Alarm-- ")

    sleep(3)

    lcd_init()


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


# Determines the 'clear' command for the OS
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
        clear_message = "clear"
        name = "Unknown"
    
    return {"name": name, "message": clear_message}


def print_debug_button_output():
    if GPIO.input(SET_BUTTON_PIN) == False:
        print("Set Button Held")
    
    if GPIO.input(HOUR_BUTTON_PIN) == False:
        print("Hour")

    if GPIO.input(MINUTE_BUTTON_PIN) == False:
        print("Minute")



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

    if err == EXIT_MESSAGE:
        # lcd_text("  WHY DID YOU  ", LCD_LINE_1)
        # lcd_text("KILL ME??? jerk ", LCD_LINE_2)

        lcd_text("  WHY DID YOU  ", LCD_LINE_1)
        lcd_text("KILL ME??? jerk ", LCD_LINE_2)

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