import random
import string

EMPTY_STRING = ''


class CharLiterals:
    """
    Common character literals used for masking or formatting.
    """
    ASTERISK = '*'
    NEWLINE = '\n'
    SPACE = ' '
    TAB = '\t'


def generate_random_string(length: int = 10) -> str:
    """Generate random string of the specified length"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def mask_secret(text: str, mask_char: str = CharLiterals.ASTERISK) -> str:
    """
    Masks all characters in the string, replacing them with mask_char,
    leaving spaces unchanged.

    :param text: The string to be masked.
    :param mask_char: The character to use for masking.
    :return: The masked string.
    """
    return ''.join([mask_char if s.strip() else s for s in text])
