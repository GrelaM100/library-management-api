import random

def random_six_digit_number():
    number = random.randint(100000, 999999)
    return str(number)