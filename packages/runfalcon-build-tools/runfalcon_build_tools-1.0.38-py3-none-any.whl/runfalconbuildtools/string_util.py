import random
import string

def get_random_string(length):
    letters = string.ascii_lowercase
    ramdom_string = ''.join(random.choice(letters) for i in range(length))
    return ramdom_string
