import random
import string
from random import randint


# Logic to shorten long url
def shorten_url():
    short_url_length = randint(4, 6)
    sc_alph_len = 26
    uc_alph_len = 26
    digits = 10
    # create a character set for creating shortened url of alphanumerics
    character_set = string.printable[:sc_alph_len + uc_alph_len + digits]
    shortened_url = str()
    for i in range(short_url_length):
        shortened_url += random.choice(character_set)
    return shortened_url
