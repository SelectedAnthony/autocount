import random
import time
import threading
import pyautogui
import keyboard
from datetime import datetime
from colorama import init, Fore, Style

# Initialize colorama for colored console output
init()

paused = False
stopped = False
stop_time = None
resume_time = None
random_numbers = []

# Function to toggle pause state using 'End' key
def toggle_pause():
    global paused, stopped
    if not stopped:  # End key should only work if not stopped
        paused = not paused
        status = "RUNNING" if not paused else "PAUSED"
        color = Fore.LIGHTGREEN_EX if not paused else Fore.LIGHTRED_EX
        print(f"{color}{status}{Style.RESET_ALL} - Click END to set resume and stop times.")

# Function to set new stop and resume times after the process has stopped or paused
def set_new_times():
    global stop_time, resume_time, paused, stopped

    if stopped:
        # Input for new times
        resume_time_input = input("Enter resume time (HH:MM AM/PM) or press Enter to resume immediately: ")
        stop_time_input = input("Enter stop time (HH:MM AM/PM) or press Enter to run indefinitely: ")

        # Set resume time (if provided)
        if resume_time_input:
            try:
                resume_time = datetime.strptime(resume_time_input, "%I:%M %p").time()
                print(f"Scheduled to resume at {resume_time.strftime('%I:%M %p')}")
            except ValueError:
                print("Invalid resume time format.")

        # Set stop time (if provided)
        if stop_time_input:
            try:
                stop_time = datetime.strptime(stop_time_input, "%I:%M %p").time()
                print(f"Scheduled to stop at {stop_time.strftime('%I:%M %p')}")
            except ValueError:
                print("Invalid stop time format.")

        # Reset paused and stopped
        paused = False
        stopped = False

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
        while paused:  # Wait if paused
            time.sleep(0.1)  # Small sleep to prevent tight loop
        pyautogui.typewrite(char)  # Type the character
        time.sleep(0.05)  # Delay between characters
    pyautogui.press('enter')  # Simulate pressing Enter

# Automatically handle scheduled pauses and stops
def run_scheduler():
    global paused, stopped, stop_time, resume_time  # Declare these variables as global
    while True:
        now = datetime.now()

        # Check for stop time
        if stop_time:
            stop_datetime = datetime.combine(now.date(), stop_time)
            if now >= stop_datetime:
                if paused:
                    print(f"{Fore.LIGHTRED_EX}Automatically Stopping - Didn't resume before designated stop time.{Style.RESET_ALL}")
                    stopped = True
                    set_new_times()  # Prompt for new times
                else:
                    print(f"{Fore.LIGHTRED_EX}Automatically Stopping at {stop_time.strftime('%I:%M %p')}{Style.RESET_ALL}")
                    stopped = True
                    set_new_times()  # Prompt for new times
                stop_time = None  # Reset stop time

        # Check for resume time
        if resume_time:
            resume_datetime = datetime.combine(now.date(), resume_time)
            if now >= resume_datetime:
                paused = False
                print(f"{Fore.LIGHTGREEN_EX}Resuming execution at {resume_time.strftime('%I:%M %p')}{Style.RESET_ALL}")
                resume_time = None  # Reset resume time

        time.sleep(1)

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Resuming in {i} seconds...", end='\r')
        time.sleep(1)
    print(" " * 30, end='\r')  # Clear the countdown message

def main():
    global stop_time, resume_time, random_numbers, paused, stopped

    # Initial start and stop time setup
    start_now = input("Enter start time (HH:MM AM/PM) or press Enter to start immediately: ")
    stop_now = input("Enter stop time (HH:MM AM/PM) or press Enter to run indefinitely: ")

    # Handle start time
    try:
        if start_now:
            start_time = datetime.strptime(start_now, "%I:%M %p").time()
            print(f"Counting will start at {start_time.strftime('%I:%M %p')}")
            while datetime.now().time() < start_time:
                time.sleep(1)  # Wait until the specified start time
        else:
            countdown_timer(10)  # 10-second countdown if no start time

        # Handle stop time
        if stop_now:
            stop_time = datetime.strptime(stop_now, "%I:%M %p").time()
            print(f"Scheduled to stop at {stop_time.strftime('%I:%M %p')}")

    except ValueError:
        print("Invalid time format.")
        return

    # Generate random numbers ending in 8
    random_numbers = generate_random_number_list(1, 500000)

    # Start the scheduler thread
    threading.Thread(target=run_scheduler, daemon=True).start()

    # Add a hotkey for pausing (End key)
    threading.Thread(target=lambda: keyboard.add_hotkey('end', toggle_pause)).start()

    # Main number typing loop
    for number in random_numbers:
        if stopped:
            break  # Stop if the process was automatically stopped

        while paused:  # Wait if paused
            time.sleep(0.1)

        # Type the number with delay
        type_with_delay(str(number))
        print(f"{Fore.LIGHTGREEN_EX}Successfully Sent: {number}{Style.RESET_ALL}")  # Print confirmation message
        time.sleep(get_random_interval())  # Wait for a random interval

if __name__ == "__main__":
    main()
