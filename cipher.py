"""
Title: Application for a simple caesar cipher w/ optional file output
Author: Primus27
Version: 1.4
"""

# Import packages
import os
import re
from getpass import getuser
from sys import exit
from time import sleep
from title_generator import TitleGen


class CaesarCipher:
    """
    Prompts user to encrypt/decrypt a cipher w/ optional file output.
    """
    def __init__(self, file_out_flag=False, to_decrypt_flag=False):
        """
        Constructor method
        :param file_out_flag: Whether attributes should be output to file
        :param to_decrypt_flag: Whether the purpose is to decrypt
        """
        # Character set
        self.alpha_set = "abcdefghijklmnopqrstuvwxyz"
        self.num_set = "0123456789"

        self.file_output_flag = file_out_flag
        self.decrypt_flag = to_decrypt_flag

        # Set purpose and start message info (for feedback and file output)
        self.purpose = "decrypt" if self.decrypt_flag else "encrypt"
        self.start_message_type = "encrypted" if self.decrypt_flag \
            else "plaintext"

        # Set input message by calling message_prompt
        self.input_message = self.message_prompt()

        # Check message contains elements and prompt for appropriate shift
        # If message contains NOT only digits (letters, symbols, etc)
        if not self.input_message.isdigit():
            self.alpha_shift = self.shift_prompt("letters")
        else:
            self.alpha_shift = 0
        # If message contains digits
        if bool(re.search(r'\d', self.input_message)):
            self.num_shift = self.shift_prompt("numbers")
        else:
            self.num_shift = 0

        # User shift response sanitised for output (no negative values)
        self.formatted_shift = "{a}.{n}".format(a=(self.alpha_shift % len(
            self.alpha_set)), n=(self.num_shift % len(self.num_set)))
        # If elements haven't been shifted, remove that value
        if "0" in self.formatted_shift:
            self.formatted_shift = self.formatted_shift.replace("0", "").\
                replace(".", "")

        # Decryption shift correction (if function used for decryption)
        if self.decrypt_flag:
            self.alpha_shift = len(self.alpha_set) - self.alpha_shift
            self.num_shift = len(self.num_set) - self.num_shift

        # Altered/final message
        self.output_message = self.encrypt_decrypt_message()

    def message_prompt(self):
        """
        Prompt the user for their input message
        :return: Input message
        """
        while True:
            message = input(
                "[?] Please enter a message to {}:".format(self.purpose))
            if message != "":
                return message

    @staticmethod
    def shift_prompt(char_set_message):
        """
        Allows user to enter how much a character should be shifted by
        :param char_set_message: Declare character set to target
        :return: The shift for a specific character set
        """
        while True:
            try:
                shift_val = int(input("[?] Enter a shift for the {}:"
                                      .format(char_set_message)))
                if shift_val < 0:
                    print("[*] Shift cannot be less than zero.")
                else:
                    return shift_val
            except ValueError:
                print("[*] Input is not a number.")

    @staticmethod
    def shift_char(char, type_char, shift):
        """
        Shifts a single character a defined amount
        :param char: The character to be shifted
        :param type_char: The character set that will be used
        :param shift: The shift value
        :return: The shifted character
        """
        uppercase_flag = char.isupper()
        new_index = None  # Current position

        # Find index values for each character and match to targeted character
        for index, item in enumerate(type_char):
            if char.lower() == item:
                # New index (e.g. 0-25 for alpha characters)
                new_index = (index + shift) % len(type_char)

        # Calculate what character the new index maps to
        for index, item in enumerate(type_char):
            if new_index == index:
                return str(item).upper() if uppercase_flag else str(item)

    def encrypt_decrypt_message(self):
        """
        A function that encrypts/decrypts the plaintext/encrypted message
        :return: The encrypted/decrypted message
        """
        # Generate the encrypted/decrypted message
        new_message = ""
        for char in self.input_message:
            # Character is a letter
            if char.lower() in self.alpha_set:
                shifted_char = self.shift_char(
                    char, self.alpha_set, self.alpha_shift)

            # Character is a number
            elif char in self.num_set:
                shifted_char = self.shift_char(
                    char, self.num_set, self.num_shift)

            # Character is punctuation
            else:
                shifted_char = char
            new_message += shifted_char
        return new_message

    def output_file(self):
        """
        A function to output class attributes to a file
        """
        # Prompt for whether the input message, shift and purpose are included
        include_original_flag = yes_no_prompt(
            "[?] Do you want to include the {} message (y/n)? ".format(
                self.start_message_type))

        # Get username of current machine and set file path of desktop
        username = getuser()
        f_path = os.path.join(
            "c:/", "users", username, "desktop", "cipher.txt")

        # Open file and append
        try:
            with open(f_path, "a") as f:
                buffer = []

                # Data already exists in the file
                if os.path.exists(f_path) and os.path.getsize(f_path) > 0:
                    f.write("\n")

                if include_original_flag:
                    advanced_output = ["Input:", self.input_message, "",
                                       "Purpose: " + self.purpose.capitalize(),
                                       "Shift: " + self.formatted_shift, ""]
                    buffer.extend(advanced_output)

                simple_output = ["Output:", self.output_message, separator(
                    line=True)]
                buffer.extend(simple_output)

                # Add a carriage return at end of each value in buffer list
                f.writelines("%s\n" % line for line in buffer)
            print("[*] Saved to Desktop")

        # Inadequate permission to access location / save to location
        except PermissionError:
            print("[*] Error saving to Desktop- Permission denied")
        # Could not find desktop path
        except OSError:
            print("[*] Error saving to Desktop - Path issues\n"
                  "Path: {}".format(f_path))


def main_menu(file_output_flag):
    """
    A function for the main menu / start screen
    :param file_output_flag: Whether attributes should be output to file
    :return: Boolean on whether file is to be output and/or message decrypted
    """
    file_output_icon = "X" if file_output_flag else " "
    # Opposite of file_output_flag if user toggles
    alt_file_output_flag = False if file_output_flag else True

    choice = None
    available_choices = [1, 2, 3, 4]

    # User input invalid or not set
    while choice not in available_choices:
        try:
            print("1. Encrypt")
            print("2. Decrypt")
            print("3. Toggle file output")
            print("4. Exit")
            print("[{}] Save to Desktop".format(file_output_icon))
            print(separator(linefeed_pre=True))

            choice = int(input("[?] Option:"))
            print(separator(line=True, linefeed_post=True))

            if choice == 1:
                decrypt_flag = False
                return file_output_flag, decrypt_flag

            elif choice == 2:
                decrypt_flag = True
                return file_output_flag, decrypt_flag

            # Recursive. Calls main menu
            elif choice == 3:
                menu_result = main_menu(alt_file_output_flag)

                file_output_flag = menu_result[0]
                decrypt_flag = menu_result[1]
                return file_output_flag, decrypt_flag

            # Close application
            elif choice == 4:
                print("Application closing...")
                sleep(3)
                exit()

            else:
                print("[*] Input must be a valid number.")
        except ValueError:
            print("[*] Input must be a valid number.")
            print(separator(line=True, linefeed_post=True))


def main():
    """
    Main function
    """
    # Output title
    title = TitleGen(text="Caesar Cipher", author="Primus27").title
    print(title)

    # Application
    while True:
        # Call main menu and return params for encryption/decryption
        menu_choice = main_menu(False)
        file_out_flag = menu_choice[0]
        to_decrypt_flag = menu_choice[1]

        # Create new cipher object and output to a file if enabled
        new_cipher = CaesarCipher(file_out_flag, to_decrypt_flag)
        if file_out_flag:
            new_cipher.output_file()

        # Display encrypted/decrypted message to terminal
        print(separator(linefeed_pre=True))
        print("{}ed message:".format(new_cipher.purpose.capitalize()))
        print(new_cipher.output_message)
        print(separator(line=True, linefeed_post=True))


def yes_no_prompt(feedback):
    """
    A yes/no prompt to eliminate repeated code
    :param feedback: Message to be displayed
    :return: A response of either yes or no
    """
    while True:
        response = input(feedback.lower())
        if response in ["yes", "y"]:
            return True
        elif response in ["no", "n"]:
            return False


def separator(line=False, linefeed_pre=False, linefeed_post=False):
    """
    Function to return elements to distinguish menu sections
    :param line: Bool for a dashed line
    :param linefeed_pre: Bool for a linefeed before the dashed line
    :param linefeed_post: Bool for a linefeed after the dashed line
    """
    separator_str = ""
    if linefeed_pre:  # Empty print statement does a carriage return
        separator_str += ""
    if line:
        separator_str += "------------------------------------------------" \
                         "-------------------------------------------"
    if linefeed_post:
        separator_str += "\n"
    return separator_str


if __name__ == '__main__':
    main()
