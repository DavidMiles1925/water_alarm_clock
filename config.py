#   These two variables determine default alarm time.
#       ALARM_HOUR:ALARM_MINUTE
ALARM_HOUR = 5
#       Set to an integer between 0 and 23
ALARM_MINUTE = 0
#       Set to an integer between 0 and 59


ALARM_SET = True
#   Alarm on/off by default.
#       Set True for ALARM: ON
#       Set False for ALARM: OFF


ALARM_DURATION = 0.1    
#   Time in seconds the pump will run.
#       In one second approx. 2oz of water comes through pump.


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


BYPASS_SET_TIME = False 
#   This variable is used to bypass setting the time on power-up
#       False:  User will set system time manually
#       True:   System time will be set to default


BYPASS_INSTRUCTIONS = False 
#   This variable is used to bypass set-time instructions.
#       *Note: If BYPASS_SET_TIME is set to True,
#       this variable will have no effect.
#
#       False:  Instructions will display at startup
#       True:   Instructions will NOT display at startup