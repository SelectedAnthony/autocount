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
    resume_time_input = input("Enter resume time (HH:MM AM/PM) or leave empty to continue paused: ")
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
            time.sleep(0.1)  # Brief sleep to prevent tight loop
        pyautogui.typewrite(char)  # Type the character
        time.sleep(0.05)  # Delay between characters
    pyautogui.press('enter')  # Simulate pressing Enter

# Automatically handle scheduled pauses and stops
def run_scheduler():
    global paused
    while True:
        now = datetime.now()

        # Check for stop time
        if stop_time:
            stop_datetime = datetime.combine(now.date(), stop_time)
            if now >= stop_datetime:
                print(f"{Fore.LIGHTRED_EX}Automatically Stopping - Didn't resume before designated stop time.{Style.RESET_ALL}")
                paused = True  # Pause execution
                stop_time = None  # Reset stop time

        # Check for resume time
        if resume_time:
            resume_datetime = datetime.combine(now.date(), resume_time)
            if now >= resume_datetime:
                paused = False
                print(f"{Fore.LIGHTGREEN_EX}Resuming execution at {resume_time.strftime('%I:%M %p')}{Style.RESET_ALL}")
                resume_time = None  # Reset resume time

        time.sleep(1)

def main():
    global stop_time, resume_time
    threading.Thread(target=lambda: keyboard.add_hotkey('end', toggle_pause)).start()

    start_now = input("Type '.start' to begin counting: ").strip().lower()

    if start_now != '.start':
        print("You must type '.start' to begin.")
        return

    print(f"{Fore.LIGHTGREEN_EX}Resuming in 10 seconds...{Style.RESET_ALL}")
    time.sleep(10)  # Wait for 10 seconds before starting

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
