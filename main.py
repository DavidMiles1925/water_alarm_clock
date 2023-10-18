try:
    from utils import \
        DEFAULT_ERROR,\
        EXIT_MESSAGE,\
        get_current_time,\
        get_os_info,\
        print_error,\
        run_clock,\
        sleep
except:
    print("ERROR LOADING IMPORTS")

if __name__ == "__main__":
    try:
        start_time = get_current_time()
        
        os_info = get_os_info()
        os_name = os_info["name"]
        sys_clr_msg = os_info["message"]

        run_clock(os_name, True)

    except:
        print_error(DEFAULT_ERROR)
        sleep(3)

    finally:
        stop_time = get_current_time()
        stop_time_display = "Stop Time:" + stop_time.strftime("%H:%M:%S")
        start_time_display = "Start Time:" + start_time.strftime("%H:%M:%S")
        print_error(EXIT_MESSAGE, start_time_display, stop_time_display)

