
import RPi.GPIO as GPIO

from settime import set_system_time

from config import BYPASS_SET_TIME

from utils import \
    DEFAULT_ERROR,\
    EXIT_MESSAGE,\
    get_current_time,\
    get_os_info,\
    lcd_error,\
    print_error,\
    run_clock,\
    setup_pins

from logger import console_and_log



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

    except Exception as e:
        lcd_error()

        print_error(DEFAULT_ERROR)

    except KeyboardInterrupt:
        console_and_log("Ctrl+C was pressed. System will exit.")

    finally:
        # Display exit message
        print_error(EXIT_MESSAGE)

        GPIO.cleanup()
        console_and_log("GPIO cleaned up.")

        exit(0)