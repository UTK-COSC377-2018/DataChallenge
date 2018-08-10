import os

"""
This file is a driver file to make it easier to run this directory's
code from the bash script.
"""

print("Enter the relative or absolute path to the TXT file that contains the JSONs you want to use.")
fname = input(">>> ")

fname = os.path.abspath(fname)

print("Enter the number of JSONs you want to use or enter -1 for default.")
numJsons = int(input(">>> "))

if numJsons != -1:
    os.system("python researchEngine.py {0:s} {1:d}".format(fname, numJsons))
else:
    os.system("python researchEngine.py {0:s}".format(fname))
