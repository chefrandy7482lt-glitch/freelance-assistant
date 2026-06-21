"""
PRICING ENGINE (FINAL CONSISTENT VERSION)

RULES:
- This file is the ONLY pricing interface
- It exposes: price()
- It consumes: tdu_value
- It does NOT generate values
"""

class PricingEngine:

    def price(self, tdu_value: float, tier: str):

        tier_map = {
            "free": 0.0,
            "scholarship": 0.0,
            "standard": 1.0,
            "power": 1.8
        }

        if tier not in tier_map:
            raise ValueError("Invalid tier")

        multiplier = tier_map[tier]

        return {
            "tier": tier,
            "tdu_value": tdu_value,
            "final_price": round(tdu_value * multiplier, 2)
        }


if __name__ == "__main__":

    engine = PricingEngine()

    print(engine.price(100, "free"))
    print(engine.price(100, "scholarship"))
    print(engine.price(100, "standard"))
    print(engine.price(100, "power"))