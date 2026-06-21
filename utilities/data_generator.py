import random
import string
import time
from datetime import datetime

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

def generate_user_name():
    random_str = ''.join(random.choices(string.ascii_letters, k=8))
    return f"AutoUser{random_str}"


def generate_user_email():
    random_str = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"{random_str}@gmail.com"


def generate_mobile_number():
    return "9" + ''.join(random.choices(string.digits, k=9))


def generate_password():
    return "Test@123"


def unique_id():

    return datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

def generate_manufacturer_name():

    return (
        f"TechNova "
        f"{unique_id()}"
    )

def generate_mailinator_email():

    return (
        f"technova{unique_id()}"
        "@mailinator.com"
    )

def generate_batch():

    return (
        "BI"
        + ''.join(
            random.choices(
                string.digits,
                k=5
            )
        )
        + "-"
        + ''.join(
            random.choices(
                string.ascii_lowercase,
                k=6
            )
        )
    )