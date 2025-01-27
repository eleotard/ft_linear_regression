import json
import signal
import sys
from train import estimate_price


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)


def main():
    theta0 = 0
    theta1 = 0

    signal.signal(signal.SIGINT, signal_handler)
    try:
        with open("train_result.json", "r") as train_res:
            data = json.load(train_res)
        theta0 = data["theta0"]
        theta1 = data["theta1"]
    except Exception:
        pass

    mileage = input("Enter a mileage: ")
    try:
        mileage = float(mileage)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    estimated_price = estimate_price(theta0, theta1, mileage)
    print(
        f"For a car with {mileage} mileages, the estimate price is : {estimated_price:.2f}"
    )


if __name__ == "__main__":
    main()
