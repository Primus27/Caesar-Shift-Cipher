"""
Title: Application for a simple caesar cipher w/ optional file output
Author: Primus27
Version: 1.1
"""

# Import packages
from os import path
from getpass import getuser
from sys import exit
from re import search

# Declare character set
alpha_set = "abcdefghijklmnopqrstuvwxyz"
num_set = "0123456789"


def yes_no_prompt(feedback):
    """
    A yes/no prompt to eliminate repeated code
    :param feedback: Message to be displayed
    :return: A response of either yes or no
    """
    while True:
        response = input(feedback.lower())
        if response == "y" or response == "yes":
            return True
        elif response == "n" or response == "no":
            return False


def rotate_prompt(char_set_message):
    """
    Allows user to enter how much a character should be shifted by
    :param char_set_message: Declare what character set is targeted (for input)
    :return: The shift for a specific character set
    """
    while True:
        try:
            shift_val = int(input("[?] Enter a shift for {}:"
                                  .format(char_set_message)))
            if shift_val < 0:
                print("[*] Shift cannot be less than zero.")
            else:
                return shift_val
        except ValueError:
            print("[*] Input is not a number.")


def shift_char(char, type_char, shift):
    """
    Rotates a single character a defined amount
    :param char: The character to be rotated
    :param type_char: The character set that will be used
    :param shift: The shift value
    :return: The rotated character
    """
    uppercase_flag = char.isupper()
    new_index = None  # Current position
    for index, item in enumerate(type_char):
        if char.lower() == item:
            # New index (e.g. 0-25 for alpha characters)
            new_index = (index + shift) % len(type_char)
    for index, item in enumerate(type_char):
        if new_index == index:  # Map the new index to a character in the list
            if uppercase_flag:
                return str(item).upper()
            else:
                return item


def output_file(input_message, output_message, shift, decrypt_flag):
    """
    A function to output recent operations to a file
    :param input_message: The original message - can be plaintext / encrypted
    :param output_message: The altered message - can be encrypted / plaintext
    :param shift: The ROT shift value
    :param decrypt_flag: Whether decryption was performed
    """
    if decrypt_flag:
        feedback = "encrypted"
        purpose = "Purpose: Decrypt"
    else:
        feedback = "plaintext"
        purpose = "Purpose: Encrypt"

    print(separator(carriage_pre=True))
    include_original_flag = yes_no_prompt("[?] Do you want to include the {} "
                                          "message (y/n)? ".format(feedback))

    username = getuser()
    f_path = path.join("c:/", "users", username, "desktop", "cipher.txt")
    shift_formatted = "Shift: {}".format(shift)

    try:
        with open(f_path, "a") as f:
            buffer = []
            # Existing data in file
            if path.exists(f_path) and path.getsize(f_path) > 0:
                f.write("\n")
            if include_original_flag:
                advanced_output = ["Input:", input_message, "", purpose,
                                   shift_formatted, ""]
                buffer.extend(advanced_output)
            simple_output = ["Output:", output_message, separator(line=True)]
            buffer.extend(simple_output)
            # Add a carriage return at end of each value in list
            f.writelines("%s\n" % line for line in buffer)
        print("[*] Saved to Desktop")
    # Inadequate permission to access location
    except PermissionError:
        print("[*] Error saving to Desktop- Permission denied")
    # Could not find desktop
    except OSError:
        print("[*] Error saving to Desktop - Path issues")
        print("Path: {}".format(path))


def title_card():
    """
    A function to display the title card / credits
    """
    print("  _____       _         _   _ _         _   _                _____ _       _               ")
    print(" / ____|     | |       | | (_) |       | | (_)              / ____(_)     | |              ")
    print("| (___  _   _| |__  ___| |_ _| |_ _   _| |_ _  ___  _ __   | |     _ _ __ | |__   ___ _ __ ")
    print(" \___ \| | | | '_ \/ __| __| | __| | | | __| |/ _ \| '_ \  | |    | | '_ \| '_ \ / _ \ '__|")
    print(" ____) | |_| | |_) \__ \ |_| | |_| |_| | |_| | (_) | | | | | |____| | |_) | | | |  __/ |   ")
    print("|_____/ \__,_|_.__/|___/\__|_|\__|\__,_|\__|_|\___/|_| |_|  \_____|_| .__/|_| |_|\___|_|   ")
    print("                                                                    | |                    ")
    print(" By Primus27                                                        |_|                    ")
    print()


def encrypt_message(file_output_flag, decrypt_flag=False):
    """
    A function that encrypts/decrypts the plaintext/encrypted message
    :param file_output_flag: Whether the message should be saved to a file
    :param decrypt_flag: A flag for when the function is used for decryption
    :return: The encrypted/decrypted message
    """
    # Input message
    purpose = "encrypt"
    if decrypt_flag:
        purpose = "decrypt"
    while True:
        message = input("[?] Please enter a message to {}:".format(purpose))
        if message != "":
            break

    # Check message contains elements and input shift
    if not message.isdigit():  # If message is not only digits
        alpha_shift = rotate_prompt("letters")
    else:
        alpha_shift = 0
    if bool(search(r'\d', message)):  # Regex. If message contains digits...
        num_shift = rotate_prompt("numbers")
    else:
        num_shift = 0

    # User shift response sanitised for output (no negative values)
    user_input_shift = (alpha_shift % len(alpha_set), num_shift % len(num_set))

    # Decryption shift correction (if function used for decryption)
    if decrypt_flag:
        alpha_shift = len(alpha_set) - alpha_shift
        num_shift = len(num_set) - num_shift

    # Generate the encrypted/decrypted message
    new_message = ""
    for char in message:  # Characters in original message
        if char.lower() in alpha_set:
            shifted_char = shift_char(char, alpha_set, alpha_shift)
        elif char in num_set:
            shifted_char = shift_char(char, num_set, num_shift)
        else:
            shifted_char = char
        new_message += shifted_char

    # Output encrypted message to terminal
    print(separator(carriage_pre=True))
    print("{}ed message:".format(purpose.capitalize()))
    print(new_message)

    # Save to file
    if file_output_flag:
        shift = "{a}.{n}".format(a=user_input_shift[0], n=user_input_shift[1])
        output_file(message, new_message, shift, decrypt_flag)

    # Call main menu
    print(separator(line=True, carriage_post=True))
    main_menu(False)


def separator(line=False, carriage_pre=False, carriage_post=False):
    """
    Function to return ASCII elements to distinguish menu sections
    :param line: Bool for a dashed line
    :param carriage_pre: Bool for a carriage return before the line
    :param carriage_post: Bool for a carriage return after the line
    """
    separator_str = ""
    if carriage_pre:  # Empty print statement does a carriage return
        separator_str += ""
    if line:
        separator_str += "------------------------------------------------" \
                         "-------------------------------------------"
    if carriage_post:
        separator_str += "\n"
    return separator_str


def decrypt_message(file_output_flag):
    """
    Function that calls the encrypt message with a flag to perform decryption
    :param file_output_flag: A flag for whether the message should be saved to
                            a file (passthrough)
    """
    encrypt_message(file_output_flag, True)  # True used as decryption flag


def main_menu(file_output_flag):
    """
    A function for the main menu / start screen
    :param file_output_flag: A flag for whether the message should be saved
                            to a file
    """
    file_output_icon = " "
    if file_output_flag:
        file_output_icon = "X"

    choice = None
    available_choices = [1, 2, 3, 4]

    while choice not in available_choices:
        try:
            print("1. Encrypt")
            print("2. Decrypt")
            print("3. Toggle file output")
            print("4. Exit")
            print("[{}] File output".format(file_output_icon))
            print(separator(carriage_pre=True))

            choice = int(input("[?] Option:"))
            print(separator(line=True, carriage_post=True))

            if choice == 1:
                encrypt_message(file_output_flag)
            elif choice == 2:
                decrypt_message(file_output_flag)
            elif choice == 3:
                if file_output_flag:
                    main_menu(False)
                else:
                    main_menu(True)
            elif choice == 4:
                exit("Application closing...")
            else:
                print("[*] Input must be a valid number.")
        except ValueError:
            print("[*] Input must be a valid number.")
            print(separator(line=True, carriage_post=True))


if __name__ == '__main__':
    title_card()
    main_menu(False)
