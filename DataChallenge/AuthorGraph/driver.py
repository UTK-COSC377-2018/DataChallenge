import sys
from ExpertPicker import *

fnames = input("Enter the JSON files to be used for determining experts. You can either enter the relative or absolute paths of the individual files, separated by spaces, or the relative or absolute path to the directory that holds all your JSONs: ")

fnames = fnames.split()

fnames = [ f for f in fnames if f != "" ]

if len(fnames) == 1:
    fnames = fnames[0]

print()
changePct = input("By default, the top 5% of authors in a field or said to be experts. Would you like to change this percentage? (yes/no)\n")

pct = 0.05

if changePct[0] == "y":
    newPct = input("Enter the new percentage in decimal form: ")
    pct = float(newPct)

expert = ExpertPicker(fnames, pct)

print()
fos = input("Type the field of study that you want to see the experts for.\nIf you want to see the experts across all fields, type \"All\".\nWhen you're done, type \"quit()\".\n")

while fos != "quit()":
    print()
    if fos == "All" or fos == "all":
        expert.printExperts()
    else:
        expert.printFieldExperts(fos)
    fos = input("Type the field of study that you want to see the experts for.\nIf you want to see the experts across all fields, type \"All\".\nWhen you're done, type \"quit()\".\n")

print()
