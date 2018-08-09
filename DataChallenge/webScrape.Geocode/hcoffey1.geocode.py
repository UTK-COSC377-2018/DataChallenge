"""
Name: Hayden Coffey
netID: hcoffey1
Assignment: COSC377 Honors, ORNL Data Challenge

The below program uses the csv output of the hcoffey1.webScrape program and geocodes it
from the provided street addresses to lat/lng coordinates using Google Maps API.
Data is exported in JSON format.
The API Key has been left blank in this version.

The purpose of this project was to create a data base my team members could use for the
geographical representation of the research paper publications.  
The generated data would be used quickly pull up coordinates of universities
from the provideded ORNL Data Challenge data base
"""
import urllib, json
import pandas as pd
from urllib.request import urlopen

#Load any previously geocoded values
jsonFile = open('universitycoordinates.json', 'r')
json_data = json.load(jsonFile)
jsonFile.close()

#open csv, and specify API Key
uniDF = pd.read_csv("university_list.csv")
API = "YourAPIKeyHere"


allowed_errorRate = []	#Tracks error rate in data ranges processed and stored
error_ranges = []		#Tracks ranges with too high error rate for use
temp_dict = {}			#Geocode values are stored until % error is evaluated

counter = 0				#Number of universities geocoded
errors = 0				#Number of API errors encountered
save_error = 0			#Number of errors in current range being geocoded

#Parameters for function
process_amount = 6000 	#How many universities to geocode
tol = 50 				#Allowed max %error 
save_point = 200 		#How many to geocode before checking %error


#Loop to geocode specified number of data values
for i in range(process_amount):

	#Pull postal data from json
	name = uniDF.iloc[i]['University']
	address = str(uniDF.iloc[i]['Street Address'])
	locality = uniDF.iloc[i]['Locality']
	address += ' ' + str(locality)
	parse_address = address.split(' ')
	parse_address = '+'.join(parse_address)

	#Make Geocode API request
	url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + parse_address + "&key=" + API

	#Process results
	try:
		with urlopen(url) as request:
			jsonPage = json.loads(request.read())
			coord = jsonPage['results'][0]['geometry']['location']

			#add data to temporary json structure 
			temp_dict[name] = {"lat":coord["lat"],"lng":coord["lng"]}
	except:
		temp_dict[name]={"lat":"nan", "lng":"nan"}
		errors+=1
		save_error+=1

	counter+=1
	print("{} processed".format(counter))

	#Evaluate data processed at specified intervals, keep if error rate is acceptable
	if counter % save_point == 0:
		temp_error = (save_error*1.0/save_point)*100 

		if temp_error > tol:
			print("ERROR: Too high error rate to commit {}%".format(temp_error))
			error_ranges.append(str(counter-save_point) + '-' + str(counter))
		else:
			print("Checkpoint: Saving Data")
			allowed_errorRate.append(temp_error)
			json_data.update(temp_dict)
			with open('universitycoordinates.json', 'w') as f:
				json.dump(json_data, f)

		temp_dict.clear()
		save_error=0
	

#write json to file
#format (name : {lat, lng})
with open('universitycoordinates.json', 'w') as f:
	json.dump(json_data, f)
	json.dump(tdata, output)


#Uncomment to view json data in terminal
#print(json.dumps(json_data, indent=4, sort_keys=True))

#Print error report of data
try:
	print("{} Data Values in JSON".format(len(json_data)))
	print("{}% total error rate.".format((errors*1.0/counter)*100))
	print("{}% error in stored data.".format(sum(allowed_errorRate)*1.0/len(allowed_errorRate)))
	print("Ranges not added to data (TOO HIGH ERROR):")
	print(error_ranges)
except:
	print("Error calculating accuracy")

csv.close()
