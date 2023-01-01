from datetime import datetime
import subprocess

def get_test_time():
    now = datetime.now()
    
    print(f"TEST TIME: {now}")
    return now

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

    print(f"Date String: {date_string}")
    return date_string

def modify_single_digit_time(digit):
    if digit < 10:
        new_digit = f"0{digit}"
    else:
        new_digit = str(digit)
    
    return (new_digit)

def press_enter_to_continue():
    print("Press Enter...")
    input("")

if __name__ == "__main__":
    year = 2023
    month = 1
    date = 1
    hour = 0
    minute = 0

    print("SYSTEM TIME TEST")
    press_enter_to_continue()

    system_time_string = create_date_string(year, month, date, hour, minute)

    #os.system(f'sudo time --set "{system_time_string}"')
    #os.system(f'sudo date -s {system_time_string}')
    subprocess.run(["sudo", "date", "-s", system_time_string])

    press_enter_to_continue()

    get_test_time()

    press_enter_to_continue()