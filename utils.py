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
    import sys
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
        SNOOZE_COUNT_CONFIG,\
        LED_PIN,\
        RELAY_PIN,\
        SET_BUTTON_PIN,\
        ALARM_BUTTON_PIN,\
        HOUR_BUTTON_PIN,\
        MINUTE_BUTTON_PIN,\
        BUTTON_SLEEP_TIME_AFTER_PRESS
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
    print("ERROR LOADING LCD RESOURCES: utils.py")

try:
    from logger import console_and_log
except:
    print(("ERROR LOADING LOGGER: main.py"))


VERSION = 1.1
AUTHOR = "David Miles"

LCD_PIN_ARRAY = [LCD_E, LCD_RS, LCD_D4, LCD_D5, LCD_D6, LCD_D7]
BUTTON_ARRAY = [ALARM_BUTTON_PIN, SET_BUTTON_PIN, HOUR_BUTTON_PIN, MINUTE_BUTTON_PIN]


########################
########################
###                  ###
###    GPIO SETUP    ###
###                  ###
########################
########################


# Set up pins for all components
def setup_pins():
    try:

        # Board Mode: BCM
        GPIO.setmode(GPIO.BCM)

        # Disable Warnings
        GPIO.setwarnings(False)

        for x in range(len(LCD_PIN_ARRAY)):
            GPIO.setup(LCD_PIN_ARRAY[x], GPIO.OUT)
            console_and_log(f"GPIO pin {LCD_PIN_ARRAY[x]} was set up as an LCD output pin.")

        for y in range(len(BUTTON_ARRAY)):
            GPIO.setup(BUTTON_ARRAY[y], GPIO.IN)
            console_and_log(f"GPIO pin {BUTTON_ARRAY[y]} was set up as an input pin.")

        # Initialize LCD screen
        lcd_init()

        # LED
        GPIO.setup(LED_PIN, GPIO.OUT)
        GPIO.output(LED_PIN, GPIO.LOW)
        console_and_log(f"GPIO pin {RELAY_PIN} was set up as an LCD output pin.")

        # Relay
        GPIO.setup(RELAY_PIN, GPIO.OUT)
        GPIO.output(RELAY_PIN, GPIO.LOW)
        console_and_log(f"GPIO pin {RELAY_PIN} was set up as an LCD output pin.")
    
    except Exception as e:
        console_and_log(f"Error occurred setting up pins: {e}")


#############################
#############################
###                       ###
###  MAIN CLOCK FUNCTION  ###
###                       ###
#############################
#############################

# Becomes true when the alarm sounds, 
# and remains true for 60 seconds. This prevents the
# alarm from sounding again during the same minute.
RECENTLY_SOUNDED = False

# Becomes True when the alarm sounds
SNOOZING = False

# Snoozing will stop when SNOOZE_COUNT = SNOOZE_COUNT_CONFIG
SNOOZE_COUNT = 0
DELAY_TIME = ((60 / SNOOZE_COUNT_CONFIG) - 1)

if DELAY_TIME > 30:
    DELAY_TIME = 30

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

    except KeyboardInterrupt:
        console_and_log("Control+C was pressed. run_clock() terminated")
        clear
        lcd_init()

    except Exception as e:
        console_and_log(f"An error occured in the run_clock() function: {e}")


########################
########################
###                  ###
###   Alarm Tools    ###
###                  ###
########################
########################
pump_primer_on = False

# Check if the 'set' button is being pressed.
def check_button_press():
    try:
        global pump_primer_on

        if (GPIO.input(ALARM_BUTTON_PIN) == False and GPIO.input(SET_BUTTON_PIN) == False):
            console_and_log("Exit button combination pressed.")
            lcd_init()
            lcd_text("PROGRAM STOPPED:", LCD_LINE_1)
            lcd_text(" RESTART DEVICE ", LCD_LINE_2)
            GPIO.cleanup()
            console_and_log("GPIO cleaned up, system exiting.")
            exit(0)

        # Check if priming function is activated.
        if (GPIO.input(HOUR_BUTTON_PIN) == False and GPIO.input(MINUTE_BUTTON_PIN) == False) and GPIO.input(SET_BUTTON_PIN):
            console_and_log("Primer activated.")

            while (GPIO.input(HOUR_BUTTON_PIN) == False and GPIO.input(MINUTE_BUTTON_PIN) == False) and GPIO.input(SET_BUTTON_PIN):
            
                # Turn on LED
                GPIO.output(LED_PIN, GPIO.HIGH)

                # Turn on Relay
                GPIO.output(RELAY_PIN, GPIO.HIGH)
                

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
            global SNOOZE_COUNT

            if SNOOZING == True:
                timer_time = (SNOOZE_COUNT_CONFIG - SNOOZE_COUNT) * DELAY_TIME
                snooze_cancel_timer = Timer(timer_time, reset_snooze_count())
                snooze_cancel_timer.start()
                SNOOZING = False
                SNOOZE_COUNT = 100

            # Add an hour when the button is pressed
            if GPIO.input(HOUR_BUTTON_PIN) == False:
                global ALARM_HOUR
                ALARM_HOUR = ALARM_HOUR + 1
                if ALARM_HOUR == 24:
                    ALARM_HOUR = 0
                sleep(BUTTON_SLEEP_TIME_AFTER_PRESS)
            
            # Add a minute when the button is pressed
            if GPIO.input(MINUTE_BUTTON_PIN) == False:
                global ALARM_MINUTE
                ALARM_MINUTE = ALARM_MINUTE + 1
                if ALARM_MINUTE == 60:
                    ALARM_MINUTE = 0
                sleep(BUTTON_SLEEP_TIME_AFTER_PRESS)


        # Turn alarm on/off when button is pressed
        if GPIO.input(ALARM_BUTTON_PIN) == False:
            global ALARM_SET
            ALARM_SET = not ALARM_SET
            console_and_log(f"Alarm status set to {ALARM_SET}")
            if ALARM_SET:
                console_and_log(f"Alarm set for {create_alarm_string(ALARM_HOUR, ALARM_MINUTE)}")
            sleep(BUTTON_SLEEP_TIME_AFTER_PRESS)

    except Exception as e:
        console_and_log(f"Error triggered from utils.check_button_press: {e}")


# Check to see if alarm needs to sound.
def check_sound_alarm(current_time):
    try:

        # This variable is set to True when
        # the pump needs to be activated.
        ALARM_SOUNDING = False

        global RECENTLY_SOUNDED
        global SNOOZING

        if ALARM_SET == True and RECENTLY_SOUNDED == False:

            # Check that alarm time matches application time.
            if current_time.hour == ALARM_HOUR and current_time.minute == ALARM_MINUTE:

                # Is the 'set alarm' button NOT being held?
                if GPIO.input(SET_BUTTON_PIN):
                    ALARM_SOUNDING = True

                    # Turn on LED
                    GPIO.output(LED_PIN, GPIO.HIGH)

                    # Turn on Relay
                    GPIO.output(RELAY_PIN, GPIO.HIGH)

                    console_and_log("ALARM SOUNDING")
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

            if SNOOZE_COUNT <= SNOOZE_COUNT_CONFIG:
                SNOOZING = True
            
            snooze_timer = Timer(DELAY_TIME, snooze_check)
            snooze_timer.start()

            # Set recently_sounded to True
            RECENTLY_SOUNDED = True

            # Start timer to prevent pump from activating again immediately.
            recently_sounded_timer = Timer(60, set_recently_sounded)
            recently_sounded_timer.start()

            # Give the circuit time to recover before initializing screen.
            sleep(0.1)

            # Re-initialize screen to deal with any voltage spike interference.
            lcd_init()
    except Exception as e:
        console_and_log(f"An error occured in the check_sound_alarm function: {e}")


# Build the string that will be displayed
# on the second line of the LCD screen.
def create_alarm_string(hour, minute):
    try:
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
    except Exception as e:
        console_and_log(f"An error occured in the create_alarm_string function: {e}")

IS_TURNING_ON = True

# Welcome message for console.
def display_welcome(os_name, loop_bool):
    global IS_TURNING_ON

    global SNOOZING
    global RECENTLY_SOUNDED
    global SNOOZE_COUNT

    clear()

    print(f"DELAY_TIME: {DELAY_TIME}")
    print(f"SNOOZE_COUNT: {SNOOZE_COUNT}")
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

    time_to_display = time_stamp.strftime("%I:%M%p %a%m/%d")

    if time_to_display[0] == "0":
        time_list = list(time_to_display)
        time_list[0] = ""
        time_to_display = ''.join(time_list)
        time_to_display = time_to_display[:10] + " " + time_to_display[10:]

    if ALARM_SET == True and GPIO.input(SET_BUTTON_PIN) == False:
        alarm_to_display = f"ALARM:ON {ALARM_TIME}"
    elif SNOOZING == True and SNOOZE_COUNT < SNOOZE_COUNT_CONFIG:
        time_to_display = "I LOVE TO GET   "
        alarm_to_display = " YOU WET! HURRY!"
    elif ALARM_SET == True:
        alarm_to_display = "ALARM:ON        "
    else:
        alarm_to_display = "ALARM: OFF      "
    
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
    global SNOOZING
    global SNOOZE_COUNT

    RECENTLY_SOUNDED = False
    SNOOZING = False
    SNOOZE_COUNT = 0

def snooze_check():
    global SNOOZING
    global RECENTLY_SOUNDED
    global SNOOZE_COUNT
    
    if SNOOZING == True:
        RECENTLY_SOUNDED = False
        SNOOZE_COUNT = SNOOZE_COUNT + 1

def reset_snooze_count():
    global SNOOZE_COUNT

    SNOOZE_COUNT = 0


def display_welcome_lcd():
    lcd_init()

    console_and_log("Welcome screen displayed")

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
        clear_message = "clear"
        name = "Unknown"
    
    return {"name": name, "message": clear_message}



######################################
######################################
###                                ###
###  Error Handling and Debugging  ###
###                                ###
######################################
######################################

DEFAULT_ERROR = "An unexpected error occured. Fuck."
EXIT_MESSAGE = "Thank you for using!"
OS_ERROR = "ERROR:\nOS not supported.\nCurrently supported operating systems:\n\t*Windos\n\t*MacOS\n\t*Linux"
GET_TIME_ERROR = "SOMETHING WENT WRONG WHILE GETTING THE SYSTEM TIME.\n Restart System."

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
    console_and_log(err)
    print("\n")
    print("**********************************************************************")

    if msg1 != "":
        console_and_log(f"{msg1}\n")
    if msg2 != "":
        console_and_log(f"{msg2}\n")

    clear()
    lcd_init()


def lcd_error():
    lcd_init()
    lcd_text("Error:", LCD_LINE_1)
    lcd_text("Restart System", LCD_LINE_2)


# Displays an on-screen message to show which button is being depressed.
def print_debug_button_output():
    if GPIO.input(SET_BUTTON_PIN) == False:
        print("Set Button Held")
    
    if GPIO.input(HOUR_BUTTON_PIN) == False:
        print("Hour")

    if GPIO.input(MINUTE_BUTTON_PIN) == False:
        print("Minute")


def restart_program():
    console_and_log("restart_program() function triggered.")
    my_app = sys.executable
    os.execl(my_app, my_app, *sys.argv)