import json

def check_user_input(input):
    try:
        mileage = float(input)
        return 1
    except mileageueError:
        print("ERROR : please enter a number")
        return 0
    except:
        print("Unexpected error occured")
        return 0
    
mileage = input("Enter a mileage: ")
while not check_user_input(mileage):
    mileage = input("Enter a mileage: ")

teta0 = 0.0
teta1 = 0.0

try:
    with open("train_result.json", 'r') as train_res:
        data = json.load(train_res)
    teta0 = data["teta0"]
    teta1 = data["teta1"]
except:
    print("0")

estimatePrice(mileage) = teta0 + (teta1) * mileage
print("For a car with {mileage} mileages, the estimate price is : {estimatePrice}")





#recuperer le resultat de lautre programme jsp comment


#train.printing()


