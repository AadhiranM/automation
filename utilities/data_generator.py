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


def generate_product_name():
    random_str = ''.join(random.choices(string.ascii_letters, k=6))
    return f"Product_{random_str}"

def generate_brand_name():
    random_str = ''.join(random.choices(string.ascii_letters, k=5))
    return f"Brand_{random_str}"

def generate_sku():
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"SKU_{random_str}"