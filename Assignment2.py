attending = int(input("How many people will be attending the cookout: "))
amount = int(input("How many hot dogs will each person get: "))
needed = attending * amount
hPack = (needed + 9) // 10
bPack = (needed + 7) // 8
hLeft = (hPack * 10) - needed
bLeft = (bPack * 8) - needed

print(f"The minimum number of packages of hot dogs required is: {hPack}")
print(f"The minimum number of packages of hot dog buns required is: {bPack}")
print(f"The number of hot dogs that will be left over is: {hLeft}")
print(f"The number of hot dog buns that will be left over is: {bLeft}")