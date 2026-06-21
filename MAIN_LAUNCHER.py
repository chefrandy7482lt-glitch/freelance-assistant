from run_freelance_assistant import main as run_cli

"""
MAIN LANDING PLACE

RULES:
- ONE entry point for the system
- No guessing which file to run
- No API confusion
- No multiple starts
"""

def start():

    print("\n=================================")
    print("   FREELANCE ASSISTANT LAUNCHER")
    print("=================================")

    print("\nChoose mode:\n")

    print("1 - Run Pricing System (CLI)")
    print("2 - Exit")

    choice = input("\nEnter selection: ")

    if choice == "1":
        run_cli()

    else:
        print("\nExiting system...\n")


if __name__ == "__main__":
    start()