"""
TDU VALUE ENGINE

Purpose:
- Discover value
- Pricing engine consumes value
- No hardcoded service prices
"""

class TDUValueEngine:

    def evaluate(
        self,
        workload_score,
        automation_score,
        time_saved_score,
        complexity_score,
        market_score
    ):

        value = (
            workload_score +
            automation_score +
            time_saved_score +
            complexity_score +
            market_score
        )

        return round(value, 2)


if __name__ == "__main__":

    engine = TDUValueEngine()

    value = engine.evaluate(
        workload_score=25,
        automation_score=25,
        time_saved_score=25,
        complexity_score=25,
        market_score=25
    )

    print("TDU VALUE:", value)