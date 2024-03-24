#################################################################
#################################################################
#####                                                       #####
#####                     IMPORTANT!!!                      #####
#####                                                       #####
#####          Make sure the constant called                #####
#####                 LOG_DIRECTORY_PATH                    #####
#####              has the correct value set!               #####
#####                                                       #####
#####   Example:                                            #####
#####  "/home/[YOUR PI NAME HERE]/water_alarm_clock/logs"   #####
#####                                                       #####
#####                                                       #####
#################################################################
#################################################################


# The path that your logs will write to:
LOG_DIRECTORY_PATH = "/home/astro/water_alarm_clock/logs"


# Turn logging on/off
LOGGING_ENABLED = True

# Turn console output on/off
CONSOLE_OUTPUT_ON = True

#  Pin assignments (See lcd.py for LCD to Pin mapping)
LED_PIN = 27
RELAY_PIN = 21
SET_BUTTON_PIN = 13
ALARM_BUTTON_PIN = 26
HOUR_BUTTON_PIN = 6
MINUTE_BUTTON_PIN = 5


#   These two variables determine default alarm time.
#       ALARM_HOUR:ALARM_MINUTE
ALARM_HOUR = 5
#       Set to an integer between 0 and 23
ALARM_MINUTE = 0
#       Set to an integer between 0 and 59


# This decides whether or not the alarm will be set when the device is powered on.
ALARM_SET = True
#   Alarm on/off by default.
#       Set True for ALARM: ON
#       Set False for ALARM: OFF


#   Time in seconds the pump will run
ALARM_DURATION = 0.1    
#       In one second approx. 2oz of water comes through pump.


# Used for determining how the snooze will function. Read below for more details.
SNOOZE_COUNT_CONFIG = 1
#   if SNOOZE_COUNT_CONFIG = 1: 
#       Pump will activate once more, in addition to intial alarm.
#        The number of seconds between the intial alarm and the
#        snooze alarm is determined by MAX_SNOOZE_TIME.
#       
#   if SNOOZE COUNT CONFIG = 
#             2:  Alarm will sound at +29 seconds and +58 seconds
#             3:  Alarm will sound at +19, +38 seconds and +57 seconds
#             4:  Alarm will sound +14, +28, +42, and +56 seconds
#             5+: Use Algorithm: DELAY_TIME = ((60 / SNOOZE_COUNT_CONFIG) - 1)


MAX_SNOOZE_TIME = 30        
#   The time in seconds between the intial alarm and the
#       snooze alarm when SNOOZE_COUNT_CONFIG = 1


#   This variable is used to bypass setting the time on power-up
BYPASS_SET_TIME = False 
#   If set to 'True', the time will be pulled from the Wifi, or if there is no connection, it will be set to the epoc.
#       False:  User will set system time manually
#       True:   System time will be set to default


#   This variable is used to bypass the instructions that display before setting the time.
BYPASS_INSTRUCTIONS = False 
#       *Note: If BYPASS_SET_TIME is set to True,
#       this variable will have no effect.
#
#       False:  Instructions will display at startup
#       True:   Instructions will NOT display at startup


# This is the amount of time that the buttons will 'sleep' after each press.
BUTTON_SLEEP_TIME_AFTER_PRESS = 0.05