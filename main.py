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
        lcd_error,\
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
        lcd_error()

        print_error(DEFAULT_ERROR)

    finally:
        # Display exit message
        print_error(EXIT_MESSAGE)

        GPIO.cleanup()

        exit()