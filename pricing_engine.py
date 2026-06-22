def calculate_price(value_score: float) -> float:
    if value_score <= 0:
        return 0.0

    base_rate = 12.5
    price = value_score * base_rate
    return round(price, 2)
