import pandas as pd 
import json
import sys
import random

expected_keys = {'km', 'price'}

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

try:
    df = pd.read_csv('data.csv')
except:
    print("ERROR: no dataset found.")
    sys.exit(1)

if not checkDataFrame(df):
    sys.exit(1)

df = df.dropna()
tmpθ0 = random.random()
tmpθ1 = random.random()
lear_rate = 0.0000001
m = len(df) #24
#print(m)

for i in range(10):
    added_distance_0 = 0.0
    added_distance_1 = 0.0
    #calculer la somme avec valeurs retournees par iterrows
    #iterrows retourne un tuple avec 2 elements
    for index, row in df.iterrows(): #index #Series: ligne avec valeurs associees aux noms de colonne
        predicted_price = estimatePrice(tmpθ0, tmpθ1, row['km'])
        error = predicted_price - row['price']
        added_distance_0 += abs(error)
        added_distance_1 += abs(error) * row["km"]
    tmpθ0 = (lear_rate * added_distance_0 / m)
    tmpθ1 = (lear_rate * added_distance_1 / m)

print(tmpθ0)
print(tmpθ1)

data = {
    "theta0": tmpθ0,
    "theta1": tmpθ1,
}

with open('train_result.json', 'w') as file:
    json.dump(data, file, indent=4)

#a la fin ecrit ses resultats dans un fichier temporaire
