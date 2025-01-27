import pandas as pd
import json
import sys
import random
import signal
import math
import matplotlib.pyplot as plt


# en python les objets DATAFRAME sont mutes par reference et pas par copie

expected_keys = {"km", "price"}
EPOCH_NUM = 1_000
LEARNING_RATE = 0.1
DATA_FILE_NAME = "data.csv"


def signal_handler(sig, frame):
    print("You pressed Ctrl+C!")
    sys.exit(0)


def check_data_frame(df):
    if set(df.columns) != expected_keys:
        print("ERROR: Wrong keys in the dataset.")
        return False
    for column in df.columns:
        try:
            pd.to_numeric(df[column])
        except ValueError:
            print(
                "ERROR: There are some columns in the dataset that contains none numeric values."
            )
            return False
    return True


def estimate_price(tmpθ0, tmpθ1, km):
    return tmpθ1 * km + tmpθ0

    # mean = df[column].mean()
    # std = df[column].std()


def standardize(df, column):
    nb_of_values = len(df[column])
    total = sum([el for el in df[column]])
    mean = total / nb_of_values
    variance = sum([(el - mean) ** 2 for el in df[column]]) / nb_of_values
    std = math.sqrt(variance)

    df[column] = (df[column] - mean) / std
    return mean, std


def main():
    signal.signal(signal.SIGINT, signal_handler)
    try:
        df = pd.read_csv(DATA_FILE_NAME)

        if not check_data_frame(df):
            sys.exit(1)

        m = len(df)  # 24
        if not m:
            print("ERROR: please enter values in the database file")
            sys.exit(1)

        df = df.dropna()

        data_kms_copy = [x for x in df["km"]]
        data_prices_copy = [x for x in df["price"]]

        plt.scatter(
            data_kms_copy,
            data_prices_copy,
            label="stars",
            color="green",
            marker="*",
            s=30,
        )
        plt.xlabel("km")
        plt.ylabel("Price")
        plt.title("Graph representing the evolution of a car price depending on its km")

        # standardisation par normalisation: permet de rendre les calculs plus stables
        # on sauvegarde l'ancienne moyenne et ecart type pour denormaliser plus tard
        mean_km, std_km = standardize(df, "km")
        mean_price, std_price = standardize(df, "price")

        theta0 = random.random()
        theta1 = random.random()

        for epoch in range(EPOCH_NUM):
            added_distance_0 = 0
            added_distance_1 = 0
            # calculer la somme avec valeurs retournees par iterrows
            # iterrows retourne un tuple avec 2 elements

            for _, row in df.iterrows():
                # index #Series: ligne avec valeurs associees aux noms de colonne
                predicted_price = estimate_price(theta0, theta1, row["km"])
                error = predicted_price - row["price"]
                added_distance_0 += error
                added_distance_1 += error * row["km"]
            tmpθ0 = LEARNING_RATE * (added_distance_0 / m)
            tmpθ1 = LEARNING_RATE * (added_distance_1 / m)
            theta0 -= tmpθ0
            theta1 -= tmpθ1

        theta1 = theta1 * (std_price / std_km)
        theta0 = (theta0 * std_price) - (theta1 * mean_km) + mean_price

        print(theta0)
        print(theta1)

        data = {
            "theta0": theta0,
            "theta1": theta1,
        }

        with open("train_result.json", "w") as file:
            json.dump(data, file, indent=4)

        all_data_predictions = [(theta1 * x + theta0) for x in data_kms_copy]
        for predicted, real_price, km in zip(
            all_data_predictions, data_prices_copy, data_kms_copy
        ):
            print(f"For {km}, Real price : {real_price}, Predicted : {predicted:.2f}")

        mse = (
            sum([(a - b) ** 2 for a, b in zip(data_prices_copy, all_data_predictions)])
            / m
        )

        print(f"The precision of the algorithm (MSE: Mean Squared Error) is {mse:.0f}")

        plt.plot(data_kms_copy, all_data_predictions)
        plt.show()
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
