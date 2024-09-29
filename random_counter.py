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
stop_time = None
resume_time = None

# Function to toggle pause state using 'End' key
def toggle_pause():
    global paused
    paused = not paused
    status = "RUNNING" if not paused else "PAUSED"
    color = Fore.LIGHTGREEN_EX if not paused else Fore.LIGHTRED_EX
    print(f"{color}{status}{Style.RESET_ALL} - Click END to set resume and stop times.")

# Function to set new stop and resume times
def set_new_times():
    global stop_time, resume_time
    resume_time_input = input("Enter resume time (HH:MM AM/PM) or leave empty to start immediately: ")
    stop_time_input = input("Enter stop time (HH:MM AM/PM) or leave empty to run indefinitely: ")

    # Set resume time
    if resume_time_input:
        try:
            resume_time = datetime.strptime(resume_time_input, "%I:%M %p").time()
            print(f"Scheduled to resume at {resume_time.strftime('%I:%M %p')}")
        except ValueError:
            print("Invalid resume time format.")

    # Set stop time
    if stop_time_input:
        try:
            stop_time = datetime.strptime(stop_time_input, "%I:%M %p").time()
            print(f"Scheduled to stop at {stop_time.strftime('%I:%M %p')}")
        except ValueError:
            print("Invalid stop time format.")

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

# Automatically handle scheduled pauses and stops
def run_scheduler():
    global paused
    while True:
        now = datetime.now()
        
        # Check for stop time
        if stop_time:
            stop_datetime = datetime.combine(now.date(), stop_time)

            # If the stop time is in the past today, set it for tomorrow
            if now >= stop_datetime:
                print(f"{Fore.LIGHTRED_EX}Automatically Stopping - Didn't resume before designated stop time.{Style.RESET_ALL}")
                toggle_pause()  # Pause the execution
                stop_time = None  # Reset stop time to prevent repeated pauses

        # Check for resume time
        if resume_time:
            resume_datetime = datetime.combine(now.date(), resume_time)

            # If the resume time is in the past today, set it for tomorrow
            if now >= resume_datetime:
                paused = False
                print(f"{Fore.LIGHTGREEN_EX}Resuming execution at {resume_time.strftime('%I:%M %p')}{Style.RESET_ALL}")
                resume_time = None  # Reset resume time

        time.sleep(1)

def main():
    global stop_time, resume_time
    threading.Thread(target=lambda: keyboard.add_hotkey('end', set_new_times)).start()
    
    # Schedule prompts for start and stop times
    start_time_input = input("Enter the start time (HH:MM AM/PM) or leave empty to start immediately: ")
    stop_time_input = input("Enter the stop time (HH:MM AM/PM) or leave empty to run indefinitely: ")

    start_time = None

    if start_time_input:
        try:
            start_time = datetime.strptime(start_time_input, "%I:%M %p").time()
            print(f"Scheduled to start at {start_time.strftime('%I:%M %p')}")
        except ValueError:
            print("Invalid start time format. Starting immediately.")

    # Set stop time if provided
    if stop_time_input:
        try:
            stop_time = datetime.strptime(stop_time_input, "%I:%M %p").time()
            print(f"Scheduled to stop at {stop_time.strftime('%I:%M %p')}")
        except ValueError:
            print("Invalid stop time format. Running until manually stopped.")

    if start_time:
        wait_until_start(start_time)
    else:
        print(f"{Fore.LIGHTGREEN_EX}Resuming in 10 seconds...{Style.RESET_ALL}")
        countdown_timer(10)  # Wait for 10 seconds before starting

    count_limit = 500000
    random_numbers = generate_random_number_list(1, count_limit)

    threading.Thread(target=run_scheduler, daemon=True).start()  # Start the scheduler in a separate thread

    for number in random_numbers:
        while paused:  # Wait if paused
            time.sleep(0.1)

        # Type the number with delay
        type_with_delay(str(number))

        print(f"{Fore.LIGHTGREEN_EX}Successfully Sent: {number}{Style.RESET_ALL}")  # Print confirmation message
        time.sleep(get_random_interval())  # Wait for a random interval

if __name__ == "__main__":
    main()
