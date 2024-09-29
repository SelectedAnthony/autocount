import random
import time
import threading
import pyautogui
import keyboard
from datetime import datetime, timedelta
from colorama import init, Fore, Style

# Initialize colorama for colored console output
init()

paused = False
stop_time_reached = False
stop_time = None

# Function to toggle pause state using 'End' key
def toggle_pause():
    global paused
    paused = not paused
    status = "RUNNING" if not paused else "PAUSED"
    color = Fore.LIGHTGREEN_EX if not paused else Fore.LIGHTRED_EX
    print(f"{color}{status}{Style.RESET_ALL} - Click END to {'pause' if not paused else 'resume'}")

# Generate a shuffled list of numbers ending in 8 up to 500,000
def generate_random_number_list(start, end):
    numbers = [i for i in range(start, end + 1) if i % 10 == 8]
    random.shuffle(numbers)
    return numbers

# Get a random interval between typing numbers
def get_random_interval():
    return random.uniform(0.7, 1.7)

# Delay typing each character and press 'Enter'
def type_with_delay(text):
    for char in text:
        while paused:  # Pause if paused
            time.sleep(0.1)
        pyautogui.typewrite(char)  # Type the character
        time.sleep(0.05)  # Delay between characters
    pyautogui.press('enter')  # Simulate pressing Enter

# Countdown timer for a given number of seconds
def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Activating in {i} seconds...", end='\r')
        time.sleep(1)
    print(" " * 30, end='\r')  # Clear the line

# Wait until the scheduled start time
def wait_until_start(start_time):
    now = datetime.now()
    start_datetime = datetime.combine(now.date(), start_time)

    if now > start_datetime:
        start_datetime += timedelta(days=1)  # Start the next day if the time has passed

    countdown_seconds = (start_datetime - now).total_seconds()
    print(f"Waiting to start at {start_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
    countdown_timer(int(countdown_seconds))

# Automatically handle scheduled pauses and stops
def run_scheduler():
    global stop_time_reached
    while True:
        if stop_time:  # If stop time is set
            now = datetime.now()
            stop_datetime = datetime.combine(now.date(), stop_time)

            if now > stop_datetime:
                stop_datetime += timedelta(days=1)  # Stop the next day if the time has passed
            
            if now >= stop_datetime and not paused:
                print(f"{Fore.LIGHTRED_EX}Automatically Stopping - Didn't resume before designated stop time.{Style.RESET_ALL}")
                stop_time_reached = True
                toggle_pause()  # Pause the execution
            
        time.sleep(1)

def main():
    global stop_time
    threading.Thread(target=lambda: keyboard.add_hotkey('end', toggle_pause)).start()
    
    # Schedule prompts for start and stop times
    start_time_input = input("Enter the start time (HH:MM) or leave empty to start immediately: ")
    stop_time_input = input("Enter the stop time (HH:MM) or leave empty to run indefinitely: ")

    start_time = None

    if start_time_input:
        try:
            start_time = datetime.strptime(start_time_input, "%H:%M").time()
            print(f"Scheduled to start at {start_time}")
        except ValueError:
            print("Invalid start time format. Starting immediately.")

    if stop_time_input:
        try:
            stop_time = datetime.strptime(stop_time_input, "%H:%M").time()
            print(f"Scheduled to stop at {stop_time}")
        except ValueError:
            print("Invalid stop time format. Running until manually stopped.")

    if start_time:
        wait_until_start(start_time)
    else:
        print(f"{Fore.LIGHTGREEN_EX}Resuming in 10 seconds...{Style.RESET_ALL}")
        countdown_timer(10)  # Wait for 10 seconds before starting

    count_limit = 500000
    random_numbers = generate_random_number_list(1, count_limit)

    threading.Thread(target=run_scheduler).start()  # Start the scheduler in a separate thread

    for number in random_numbers:
        while paused:  # Wait if paused
            time.sleep(0.1)

        # Type the number with delay
        type_with_delay(str(number))

        print(f"{Fore.LIGHTGREEN_EX}Successfully Sent: {number}{Style.RESET_ALL}")  # Print confirmation message
        time.sleep(get_random_interval())  # Wait for a random interval

if __name__ == "__main__":
    main()
