import random
import time
import pyautogui

def generate_random_number_list(start, end):
    numbers = list(range(start, end + 1))
    random.shuffle(numbers)
    return numbers

def insert_random_mistake(number):
    mistakes = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p']
    if random.random() < 0.05:  # 5% chance to insert a mistake
        mistake = random.choice(mistakes)
        return f"{number}{mistake}"
    return str(number)

def get_random_interval():
    return random.uniform(0.5, 3.5)

def countdown_timer(seconds):
    for i in range(seconds, 0, -1):
        print(f"Activating in {i} seconds...", end='\r')
        time.sleep(1)
    print(" " * 30, end='\r')  # Clear the line

def main():
    input("Type '.start' to begin counting: ")

    countdown_timer(20)

    count_limit = 500000
    random_numbers = generate_random_number_list(1, count_limit)

    for number in random_numbers:
        output = insert_random_mistake(number)
        print(output)
        pyautogui.typewrite(output)  # Simulate typing the output
        pyautogui.press('enter')  # Simulate pressing Enter
        time.sleep(get_random_interval())  # Wait for a random interval

if __name__ == "__main__":
    main()
