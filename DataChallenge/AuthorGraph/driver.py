import os
from ExpertPicker import *

# Asks user for the JSON files
fnames = input("Enter the TXT file containing the JSONs to be used for determining experts.\nYou can either enter the relative or absolute paths of the file.\nNote that, if using a relative path, the path must be relative to the AuthGraph directory.\n>>> ")

fnames = os.path.abspath(fnames)

print()

# Asks the user how many JSONs they want to use
numJsons = int(input("How many JSONs would you like to use?\nType \"-1\" to use default.\n>>> "))
if numJsons == -1:
    print("numJsons = -1")
    numJsons = 100
print(numJsons)
print()

# Asks the user if they want to change the percentage
changePct = input("By default, the top 5% of authors in a field or said to be experts.\nWould you like to change this percentage? (yes/no)\n")

pct = 0.05

# If the user responds "yes", asks for a new percentage and sets the value.
if changePct[0] == "y":
    newPct = input("Enter the new percentage in decimal form: ")
    pct = float(newPct)

# Determines the experts
expert = ExpertPicker(fnames, numJsons, pct)

print()
# The remainder of this code allows the user to query the results.
fos = input("Type the field of study that you want to see the experts for.\nIf you want to see the experts across all fields, type \"All\".\nIf you want to see a list of valid fields, type \"fields\".\nWhen you're done, type \"quit()\".\n>>> ")

while fos != "quit()":
    print()
    if fos == "All" or fos == "all":
        expert.printExperts()
    elif fos == "fields" or fos == "Fields":
        expert.listFields()
    else:
        expert.printFieldExperts(fos)
    fos = input("Type the field of study that you want to see the experts for.\nIf you want to see the experts across all fields, type \"All\".\nIf you want to see a list of valid fields, type \"fields\".\nWhen you're done, type \"quit()\".\n>>> ")

print()
