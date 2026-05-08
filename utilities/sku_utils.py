def generate_next_sku(sku):
    if not sku or len(sku) < 4:
        raise ValueError("Invalid SKU")

    prefix = sku[:-4]        # PRD2025X
    number = sku[-4:]        # 0007

    if not number.isdigit():
        raise ValueError("Last 4 digits must be numeric")

    next_number = str(int(number) + 1).zfill(4)

    return f"{prefix}{next_number}"