from tdu_value_engine import TDUValueEngine
from pricing_engine import PricingEngine


def main():

    print("\n=================================")
    print("      FREELANCE PRICING CLI")
    print("=================================")

    tdu = TDUValueEngine()
    pricing = PricingEngine()

    value = tdu.evaluate(
        workload_score=25,
        automation_score=25,
        time_saved_score=25,
        complexity_score=25,
        market_score=25
    )

    print(f"\nTDU VALUE: {value}\n")

    for tier in ["free", "scholarship", "standard", "power"]:
        result = pricing.price(value, tier)

        print(f"{result['tier']:12} ${result['final_price']}")

    print("\nSYSTEM: PRICING PIPELINE ACTIVE\n")


if __name__ == "__main__":
    main()