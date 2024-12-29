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
    

theta0 = 0.0
theta1 = 0.0

try:
    with open("train_result.json", 'r') as train_res:
        data = json.load(train_res)
    theta0 = data["theta0"]
    theta1 = data["theta1"]
except:
    pass
    
mileage = input("Enter a mileage: ")
while not check_user_input(mileage):
    mileage = input("Enter a mileage: ")
mileage = float(mileage)
estimatePrice = theta0 + (theta1) * mileage
print(f"For a car with {mileage} mileages, the estimate price is : {estimatePrice}")





#recuperer le resultat de lautre programme jsp comment


#train.printing()


