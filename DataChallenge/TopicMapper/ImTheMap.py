#!/usr/bin/env python3

import sys
import json
import numpy as np
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

# Ensures that every string in the list is only one word
# borrowed from Thomas Beard
def cleanUp(myList):
    rv = []
    for ob in myList:
        ob = ob.split()
        for word in ob:
            rv.append(word.lower())
    return rv

#check arguments
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print('Usage: ImTheMap.py inputFile [Line Read Limit]')
    print('Example: ImTheMap.py aminer_papers_0.txt 100000')
    print('Example: ImTheMap.py aminer_papers_0.txt')
    exit(0)

# load dictionary of schools and coordinates
schools = {}
with open("universitycoordinates.json", 'r') as f:
    js = json.load(f)
    for school in js:
        cords = js[school]
        lng = cords['lng']
        lat = cords['lat']
        if ((not np.isnan(float(lng))) and (not np.isnan(float(lat)))):
            schools[school.strip()] = (lng, lat)
    f.close()

topics = {}
count = 0
filename = sys.argv[1]
if len(sys.argv) == 3:
    limit = int(sys.argv[2])

print("generating dictionary...")
with open(filename, 'r') as f:
    for line in f:
        count += 1
        if len(sys.argv) == 3 and count > limit:
            break
        if count % 10000 == 0:
            print("Loaded", count, "papers so far")

        obj = json.loads(line)
        try:
            # get organization
            org = obj['authors'][0]['org']
			
            #find org in schools
            found = False
            for school in schools:
                if school in org:
                    found = True
                    org = school
            if not found:
                continue

            #get keywords
            keys = obj['keywords']
            keys = cleanUp(keys) #seperate into individual words
            keys = set(keys)  # convert to set to remove duplicates

            #add school to the topic, count how many instances of each school in each topic
            for key in keys:
                if key not in topics:
                    topics[key] = {org: 1}
                else:
                    if org not in topics[key]:
                        topics[key][org] = 1
                    else:
                        topics[key][org] += 1
        except:
            continue

print("dictionary ready")

# let user input topic to generate map for
print("\nEnter a topic to generate a map for: (or exit to quit)")
inpt = input().strip()
while (inpt != "exit"):
    if inpt in topics:
		#Generate Map
        map = Basemap(projection='mill',lon_0=0)
        # plot coastlines, draw label meridians and parallels.
        map.drawcoastlines()
        map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
        map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
        # fill continents 'green' (with zorder=0), color wet areas 'aqua'
        map.drawmapboundary(fill_color='aqua')
        map.fillcontinents(color='green',lake_color='aqua')
        print("Found", inpt, "at these schools:")
		#Add markers for each school
        for s in topics[inpt]:
            sch = schools[s]
            print(s, ":", topics[inpt][s], ":", sch)
            x,y = map(sch[0], sch[1])
            #map.plot(x, y, marker='D',color='m')
            map.plot(x, y, marker='o',color='r')
	
        #show map
        plt.title('Paper Locations')
        plt.show()
    else:
	    print("Could not find that topic")
    print("\nEnter a topic to generate a map for: (or exit to quit)")
    inpt = input().strip()
		

        

