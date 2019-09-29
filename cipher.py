"""
Title: Application for a simple caesar cipher
Author: Primus27
Version: 1.0
"""

# Declare character set
alpha = "abcdefghijklmnopqrstuvwxyz"
num = "0123456789"


def rotate_amount(char_set):
    """
    Allows user to enter how much a character should be shifted by
    :param char_set: Declare what character set is targeted
    :return: The shift for a specific character set
    """
    while True:
        try:
            shift_val = int(input("Enter a shift for " + char_set + ":"))
            if shift_val < 0:
                print("Shift cannot be less than zero - try again")
            else:
                return shift_val
        except ValueError:
            print("Input is not a number - try again")


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
    # Find the current index value of that letter
    for index, item in enumerate(type_char):
        if char.lower() == item:
            new_index = (index + shift) % len(type_char)  # New index (0-25)
    # Find the current index value of that letter
    for index, item in enumerate(type_char):
        if new_index == index:
            if uppercase_flag:
                return str(item).upper()
            else:
                return item


def encrypt_message(message):
    """
    A function that encrypts the plaintext message
    :param message: The plaintext message
    :return: The encrypted message
    """
    encrypted_message = ""
    for char in message:  # Characters in plaintext message
        if char.lower() in alpha:
            shifted_char = shift_char(char, alpha, alpha_shift)
        elif char in num:
            shifted_char = shift_char(char, num, num_shift)
        else:
            shifted_char = char
        encrypted_message += shifted_char
    return encrypted_message


# Input plaintext message
while True:
    plaintext = input("Please enter a message to encode:")
    if plaintext != "":
        break

# Input shift for each element
alpha_shift = rotate_amount("letters")
num_shift = rotate_amount("numbers")

# Display encrypted message
print("Encrypted message:\n" + encrypt_message(plaintext))
