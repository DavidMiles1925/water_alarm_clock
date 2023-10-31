ALARM_HOUR = 21         #   These two variables determine default alarm time.
ALARM_MINUTE = 21       #       ALARM_HOUR:ALARM_MINUTE
                        #       Set to an integer between 0 and 59

ALARM_SET = True        #   Alarm on by default
                        #       Set True for ALARM: ON
                        #       Set False for ALARM: OFF

ALARM_DURATION = 0.1 # Time in seconds the pump will run.
                        # In one second approx. 2oz of water comes through pump.


SNOOZE_COUNT_CONFIG = 1     # `SNOOZE_COUNT_CONFIG = 1`: Alarm will sound once more. 
#                               #   The number of seconds between the intial alarm and the snooze alarm 
#                                   is determined by MAX_SNOOZE_TIME.

MAX_SNOOZE_TIME = 30