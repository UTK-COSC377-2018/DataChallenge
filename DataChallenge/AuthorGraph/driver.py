import sys
from ExpertPicker import *

# Asks user for the JSON files
fnames = input("Enter the JSON files to be used for determining experts.\nYou can either enter the relative or absolute paths of the individual files, separated by spaces, or the relative or absolute path to the directory that holds all your JSONs: ")

# Converts the user input into a list of paths
fnames = fnames.split()

fnames = [ f for f in fnames if f != "" ]

# If there is only one element, converts fnames to a string.
if len(fnames) == 1:
    fnames = fnames[0]

print()
# Asks the user if they want to change the percentage
changePct = input("By default, the top 5% of authors in a field or said to be experts.\nWould you like to change this percentage? (yes/no)\n")

pct = 0.05

# If the user responds "yes", asks for a new percentage and sets the value.
if changePct[0] == "y":
    newPct = input("Enter the new percentage in decimal form: ")
    pct = float(newPct)

# Determines the experts
expert = ExpertPicker(fnames, pct)

print()
# The remainder of this code allows the user to query the results.
fos = input("Type the field of study that you want to see the experts for.\nIf you want to see the experts across all fields, type \"All\".\nIf you want to see a list of valid fields, type \"fields\".\nWhen you're done, type \"quit()\".\n>>>")

while fos != "quit()":
    print()
    if fos == "All" or fos == "all":
        expert.printExperts()
    elif fos == "fields" or fos == "Fields":
        expert.listFields()
    else:
        expert.printFieldExperts(fos)
    fos = input("Type the field of study that you want to see the experts for.\nIf you want to see the experts across all fields, type \"All\".\nIf you want to see a list of valid fields, type \"fields\".\nWhen you're done, type \"quit()\".\n>>>")

print()
