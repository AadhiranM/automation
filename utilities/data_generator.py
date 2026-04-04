import random
import string

def generate_category_name():
    random_str = ''.join(random.choices(string.ascii_letters, k=8))
    return f"AutoCat{random_str}"

def generate_variant_type():
    random_str = ''.join(random.choices(string.ascii_letters, k=5))
    return f"Type_{random_str}"


def generate_variant_value():
    random_str = ''.join(random.choices(string.ascii_letters, k=5))
    return f"Value_{random_str}"