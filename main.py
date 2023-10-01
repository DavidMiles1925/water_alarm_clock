try:
    import RPi.GPIO as GPIO
except:
    print("ERROR LOADING GPIO: main.py")

try:
    from config import BYPASS_SET_TIME
except:
    print("ERROR LOADING CONFIG: main.py")

try:
    from utils import \
        DEFAULT_ERROR,\
        EXIT_MESSAGE,\
        get_current_time,\
        get_os_info,\
        print_error,\
        run_clock,\
        sleep,\
        setup_pins
except:
    print("ERROR LOADING UTILITIES: main.py")
    exit()

try:
    from lcd import lcd_init
except:
    print("ERROR LOADING LCD RESOURCES: main.py")

try:
    from settime import set_system_time
except:
    print("ERROR LOADING SETTIME: main.py")


if __name__ == "__main__":
    try:
        setup_pins()

        if BYPASS_SET_TIME == False:
            set_system_time()

        start_time = get_current_time()
        
        os_info = get_os_info()
        os_name = os_info["name"]
        sys_clr_msg = os_info["message"]

        run_clock(os_name, True)

    except:
        print_error(DEFAULT_ERROR)
        GPIO.cleanup()
        sleep(3)

    finally:
        stop_time = get_current_time()
        stop_time_display = "Stop Time: " + stop_time.strftime("%H:%M:%S")
        start_time_display = "Start Time: " + start_time.strftime("%H:%M:%S")

        # Display exit message
        print_error(EXIT_MESSAGE, start_time_display, stop_time_display)

        lcd_init()
        GPIO.cleanup()

        exit()