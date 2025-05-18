weight = float(input("Enter your weight (LBS): "))
height = float(input("Enter your height (IN): "))
bMI = (weight * 703) / (height ** 2)
print(f"Your BMI is {bMI:.1f}") 
if bMI < 18.6:
    print("You're Underweight")
elif bMI > 24.9:
    print("You're Overweight")
else:
    print("You're Optimal Weight")
##########################################################
total = 0
for number in range (2,101,2):
    total += number
    print(total)
##########################################################
total = 0
x = int(input("Enter an odd number(smaller): "))
y = int(input("Enter an odd number(larger): "))
for number in range (x,y+1,2):
    total += number
    print(total)
##########################################################
target = float(input("Enter the target price: "))

while True:
    current = float(input("Enter current stock price: "))
    if current >= target:
        print("Shares can be sold")
        break
##########################################################
tuition = 8000
rate = 0.03
for year in range (1,6):
    tuition += tuition * rate
    print(f"Year {year}: ${tuition:.2f}")