import pandas as pd 
import json
import sys
import random

#en python les objets DATAFRAME sont mutes par reference et pas par copie

expected_keys = {'km', 'price'}
EPOCH_NUM = 50
LEARNING_RATE = 0.01

def checkDataFrame(df):
    if (set(df.columns) != expected_keys):
        print("ERROR: Wrong keys in the dataset.")
        return 0
    for column in df.columns:
        #print(df[column])
        try:
            pd.to_numeric(df[column])
        except ValueError:
            print("ERROR: There are some columns in the dataset that contains none numeric values.")
            return 0

    # if (df.dtypes['km'] != "int64" and df.dtypes['km'] != "float64") or (df.dtypes['price'] != 'int64' and df.dtypes['price'] != 'float64'):
    #     return 0
    return 1

def estimatePrice(tmpθ0, tmpθ1, mileage):
    return tmpθ1 * mileage + tmpθ0  

def standardize(df, column):
    mean = df[column].mean()
    std = df[column].std()
    #formule de la normalisation par standardisation
    #el = (el - moyenne) / ecart-type
    df[column] = (df[column] - mean) / std
    return mean, std

try:
    df = pd.read_csv('data.csv')
except:
    print("ERROR: no dataset found.")
    sys.exit(1)

if not checkDataFrame(df):
    sys.exit(1)

df = df.dropna()

#standardisation par normalisation: permet de rendre les calculs plus stables
#on sauvegarde l'ancienne moyenne et ecart type pour denormaliser plus tard
mean_km, std_km = standardize(df, 'km')
mean_price, std_price = standardize(df, 'price')
# print(df["km"])
# print(df["price"])
# print('moyennes:')
# print(df["km"].mean())
# print(df["price"].mean())

# print(mean_km)
# print(mean_price)
# print('ecarts types')
# print(df["km"].std())
# print(df["price"].std())
# print(std_km)
# print(std_price)





tmpθ0 = random.random()
tmpθ1 = random.random()
lear_rate = 0.01
m = len(df) #24
#print(m)

for epoch in range(EPOCH_NUM):
    added_distance_0 = 0.0
    added_distance_1 = 0.0
    #calculer la somme avec valeurs retournees par iterrows
    #iterrows retourne un tuple avec 2 elements
    for index, row in df.iterrows(): #index #Series: ligne avec valeurs associees aux noms de colonne
        predicted_price = estimatePrice(tmpθ0, tmpθ1, row['km'])
        error = predicted_price - row['price']
        added_distance_0 += error
        added_distance_1 += error * row["km"]
    tmpθ0 -= LEARNING_RATE * (added_distance_0 / m)
    tmpθ1 -= LEARNING_RATE * (added_distance_1 / m)

print(tmpθ0)
print(tmpθ1)

theta1 = -(tmpθ1 * std_price / std_km)
theta0 = (tmpθ0 * std_price) + mean_price - (tmpθ1 * std_price / std_km * mean_km)

data = {
    "theta0": theta0,
    "theta1": theta1,
}

with open('train_result.json', 'w') as file:
    json.dump(data, file, indent=4)

#a la fin ecrit ses resultats dans un fichier temporaire
