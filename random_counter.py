import random
import time
import pyautogui
import keyboard  # Make sure to install the keyboard module

def generate_random_number_list(start, end):
    numbers = list(range(start, end + 1))
    random.shuffle(numbers)
    return numbers

def insert_random_mistake(number):
    mistakes = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    if random.random() < 0.10:  # 10% chance to insert a mistake
        mistake = random.choice(mistakes)
        return f"{number}{mistake}", True  # Return the mistake and flag it
    return str(number), False  # No mistake, just return the number

def get_random_interval():
    return random.uniform(0.7, 2.3)

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Activating in {i} seconds...", end='\r')
        time.sleep(1)
    print(" " * 30, end='\r')  # Clear the line

def type_with_delay(text):
    for char in text:
        pyautogui.typewrite(char)  # Type each character
        time.sleep(0.05)  # Delay between characters
    pyautogui.press('enter')  # Simulate pressing Enter

def main():
    input("Type '.start' to begin counting: ")

    countdown_timer(20)

    count_limit = 500000
    random_numbers = generate_random_number_list(1, count_limit)

    paused = False

    for number in random_numbers:
        if keyboard.is_pressed('F4'):
            paused = not paused
            status = "PAUSED" if paused else "RUNNING"
            print(f"{status} - Click F4 to {'resume' if paused else 'pause'}")
            time.sleep(0.5)  # Debounce delay

        if paused:
            time.sleep(0.1)  # Sleep while paused
            continue

        output, is_mistake = insert_random_mistake(number)
        
        # Type the output with delay
        type_with_delay(output)
        
        if is_mistake:
            print(f"(Mistake) Successfully Sent: {output} - Resending")
            # Resend without the mistake
            corrected_output = str(number)
            type_with_delay(corrected_output)
        
        print(f"Successfully Sent: {output if not is_mistake else corrected_output}")  # Print confirmation message
        time.sleep(get_random_interval())  # Wait for a random interval

if __name__ == "__main__":
    main()
