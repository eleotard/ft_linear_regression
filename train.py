import pandas as pd 
import json

df = pd.read_csv('data.csv')

# print(df["km"])
# print(type(df["km"]))

data = {
    "teta0": 0.1,
    "teta1": 0.6,
}

with open('train_result.json', 'w') as file:
    json.dump(data, file, indent=4)

#a la fin ecrit ses resultats dans un fichier temporaire
