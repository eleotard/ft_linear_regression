import json
import signal
import sys


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)


def check_user_input(input):
    try:
        _ = float(input)
        return 1
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    theta0 = 0.0
    theta1 = 0.0

    signal.signal(signal.SIGINT, signal_handler)
    try:
        with open("train_result.json", "r") as train_res:
            data = json.load(train_res)
        theta0 = data["theta0"]
        theta1 = data["theta1"]
    except Exception:
        pass

    mileage = input("Enter a mileage: ")
    while not check_user_input(mileage):
        mileage = input("Enter a mileage: ")
    mileage = float(mileage)
    estimatePrice = theta0 + (theta1) * mileage
    print(f"For a car with {mileage} mileages, the estimate price is : {estimatePrice}")


if __name__ == "__main__":
    main()
