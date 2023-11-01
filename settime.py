try:
    import RPi.GPIO as GPIO
    import subprocess
except:
    print("COULD NOT LOAD PYTHON RESOURCES: settime.py")

try:
    from lcd import lcd_init, lcd_text, LCD_LINE_1, LCD_LINE_2
except:
    print("COULD NOT LOAD LCD RESOURCES: settime.py")

try:
    from utils import print_error, restart_program, sleep, GET_TIME_ERROR, HOUR_BUTTON_PIN, MINUTE_BUTTON_PIN
except:
    print("COULD NOT LOAD UTILS: settime.py")

try:
    from config import BYPASS_INSTRUCTIONS
except:
    print("COULD NOT LOAD CONFIG: settime.py")


def print_lcd_instructions():
    lcd_text("   PLEASE SET   ", LCD_LINE_1)
    lcd_text("    THE TIME    ", LCD_LINE_2)
    sleep(3)

    lcd_text("'MINUTE' button:", LCD_LINE_1)
    lcd_text("Change the value", LCD_LINE_2)
    sleep(3)

    lcd_text("'HOUR' button:  ", LCD_LINE_1)
    lcd_text(" Sets the value ", LCD_LINE_2)
    sleep(3)


def get_user_date(date_int, label, min, max):
    move_on = False

    while move_on == False:
                 #1234567890123456
        lcd_text("What is the     ", LCD_LINE_1)
        lcd_text(f"  {label}?: {date_int}", LCD_LINE_2)

        if GPIO.input(MINUTE_BUTTON_PIN) == False:
            date_int = date_int + 1
            sleep(0.1)

        if date_int > max:
            date_int = min

        if GPIO.input(HOUR_BUTTON_PIN) ==  False:
            sleep(0.2)
            return date_int
        

def create_date_string(year, month, date, hour, minute):

    # Transform variables to strings
    year = str(year)
    month = modify_single_digit_time(month)
    date = modify_single_digit_time(date)
    hour = modify_single_digit_time(hour)
    minute = modify_single_digit_time(minute)

    # "YYYY-MM-DD HH:MM:SS"
    date_string = f"{year}-{month}-{date} {hour}:{minute}:00"

    # "02301010000.00"
    #date_string = f"{month}{date}{hour}{minute}{year}.00"

    return date_string


def modify_single_digit_time(digit):
    if digit < 10:
        new_digit = f"0{digit}"
    else:
        new_digit = str(digit)
    
    return (new_digit)


def set_system_time():
    try:
        year = 2023
        month = 1
        date = 1
        hour = 0
        minute = 0

        print("USE BUTTONS AND SCREEN")

        if BYPASS_INSTRUCTIONS == False:
            print_lcd_instructions()

        year = get_user_date(year, "YEAR", 2023, 2050)
        month = get_user_date(month, "MONTH", 1, 12)
        date = get_user_date(date, "DAY", 1, 31)
        hour = get_user_date(hour, "HOUR", 0, 23)
        minute = get_user_date(minute, "MINUTE", 0, 59)

        system_time_string = create_date_string(year, month, date, hour, minute)

        result = subprocess.run(["sudo", "date", "-s", system_time_string])

        if result.returncode != 0:
            lcd_text("Not a real date.", LCD_LINE_1)
            lcd_text("Restarting...", LCD_LINE_2)
            sleep(5)
            restart_program()

        lcd_init()
        
    except KeyboardInterrupt:
        lcd_init()
        lcd_text("Error:", LCD_LINE_1)
        lcd_text("Restart System", LCD_LINE_2)

        print_error(GET_TIME_ERROR)

        GPIO.cleanup()

def press_enter_to_continue():

    print("Press Enter...")
    input("")

# def get_test_time():
#     now = datetime.now()

#     return now