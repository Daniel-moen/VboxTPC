import socket
import sys
import pyautogui
import time
from colorama import Fore, Back, Style, init

# Initialize colorama
init(autoreset=True)

# Replace with your Twitch channel name and OAuth token
channel = "maybeuncallable"
oauth_token = "oauth:fl9pg9nj690crx0p8s18dpvn6y4oh3"

# Twitch IRC server and port
host = "irc.chat.twitch.tv"
port = 6667

def connect_to_twitch():
    # Create a socket connection to the Twitch IRC server
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect((host, port))

    # Send the login credentials to Twitch IRC server
    conn.send(f"PASS {oauth_token}\r\n".encode('utf-8'))
    conn.send(f"NICK justinfan123456\r\n".encode('utf-8'))  # Use a placeholder username
    conn.send(f"JOIN #{channel}\r\n".encode('utf-8'))

    return conn

def move_relative(x, y):
    # Move the mouse relative to the current position by x, y
    print(f"{Fore.GREEN}{Style.BRIGHT}Moving {x},{y}")
    current_x, current_y = pyautogui.position()  # Get the current position

    # Define screen boundaries (width and height of your screen)
    screen_width = 2560
    screen_height = 1080

    # Calculate new position
    new_x = current_x + x
    new_y = current_y + y

    # Make sure the mouse stays within screen boundaries
    new_x = max(0, min(screen_width - 1, new_x))  # Ensure x is within [0, screen_width-1]
    new_y = max(0, min(screen_height - 1, new_y))  # Ensure y is within [0, screen_height-1]

    pyautogui.moveTo(new_x, new_y, duration=0.5)

def type_message(message):
    # Type the given message
    print(f"{Fore.YELLOW}{Style.BRIGHT}Typing message: {message}")
    pyautogui.typewrite(message, interval=0.1)

def press_button(key):
    # Press the specified button
    print(f"{Fore.CYAN}{Style.BRIGHT}Pressing button: {key}")
    pyautogui.press(key)

def scroll(amount):
    # Scroll the mouse by the specified amount
    print(f"{Fore.MAGENTA}{Style.BRIGHT}Scrolling by: {amount}")
    pyautogui.scroll(amount)

def listen_for_messages(conn):
    while True:
        response = conn.recv(2048).decode('utf-8')
        if "PING" in response:
            conn.send("PONG :tmi.twitch.tv\r\n".encode('utf-8'))
        else:
            if "PRIVMSG" in response:
                # Extract username and message from the response
                username = response.split("!")[0][1:]
                message = response.split(" :", 1)[1]

                first_char = message[0]
                print(f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}Username: {Style.BRIGHT}{Fore.GREEN}{username}{Style.RESET_ALL} | {Fore.WHITE}Message: {message}")

                if first_char == "!":
                    # Highlight the command and make it more noticeable
                    print(f"{Fore.YELLOW}{Style.BRIGHT}Command received: {Fore.CYAN}{message}")

                    # Handle the "move" command
                    if "move" in message:
                        parts = message.split(" ")
                        try:
                            x = int(parts[1].strip())  # Trim spaces before conversion
                            y = int(parts[2].strip())  # Trim spaces before conversion
                            move_relative(x, y)
                        except ValueError as err:
                            print(f"{Fore.RED}{Style.BRIGHT}Error parsing 'move' command:", err)

                    # Handle the "type" command
                    if "type" in message:
                        parts = message.split(" ")
                        message_to_type = " ".join(parts[1:])
                        type_message(message_to_type)

                    # Handle the "press" command
                    if "press" in message:
                        parts = message.split(" ")
                        button = parts[1].strip()  # Trim spaces before pressing the key
                        press_button(button)

                    # Handle the "scroll" command
                    if "scroll" in message:
                        parts = message.split(" ")
                        try:
                            amount = int(parts[1].strip())  # Trim spaces before conversion
                            scroll(amount)
                        except ValueError as err:
                            print(f"{Fore.RED}{Style.BRIGHT}Error parsing 'scroll' command:", err)

def main():
    conn = connect_to_twitch()
    listen_for_messages(conn)

if __name__ == "__main__":
    main()
