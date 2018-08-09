"""
Name: Hayden Coffey
netID: hcoffey1
Assignment: COSC377 Honors Project, ORNL Data Challenge

The program below utilizes webscraping with BeautifulSoup to grab postal/address information
of 13000+ universities from 4icu.org and store them into a csv file for later use in geocoding
the information with Google Maps API
"""
import bs4
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

#Create lists to hold university data
name = []
country = []
street_Address = []
locality = []
postal_Code = []
region = []


counter = 1	#How many universities have been scraped
p_count = 1 #What page of the website the algorithm is currently on
val = 2		#Track page url number

#Main loop to scrape data from universities
while True:
	print("Page:",p_count)
	p_count += 1

	#Grab html of main page, parse with lxml
	url_link = "https://www.4icu.org/reviews/index" + str(val) + ".htm"
	uClient = urlopen(url_link)
	page_html = uClient.read()
	uClient.close()

	page_soup = soup(page_html, 'lxml')

	#Gather list of rows with university links [Data on site is in a table], ignore header row
	t_rows = page_soup.findAll("tr")
	del t_rows[0]

	#Use embeded hyperlink in each row to pull up university page and scrape data	
	for row in t_rows:
		name.append(row.td.a.text)
		country.append(row.find("td", class_="text-right").text)

		#Grab and parse university page html
		url_2 = "https://www.4icu.org" + row.td.a['href']

		uClient = urlopen(url_2)
		uv_html = uClient.read()
		uClient.close()

		uv_soup = soup(uv_html, 'lxml')

		geo_table = uv_soup.find("div", {"itemtype":"http://schema.org/PostalAddress"}).td
		
		#Grab relevant information and store into respective list
		street_Address.append(geo_table.find("span", {"itemprop":"streetAddress"}).text)
		locality.append(((geo_table.find("span", {"itemprop":"addressLocality"}).text).split(' '))[0])
		postal_Code.append(geo_table.find("span", {"itemprop":"postalCode"}).text)
		region.append(geo_table.find("span", {"itemprop":"addressRegion"}).text)

		print("{} universities processed!".format(counter))
		counter+=1

	#Do not exceed total number of pages on main hub
	val+=1
	if val == 28:
		break

#Create pandas dataframe and convert to csv and export
df = pd.DataFrame(name, columns=['University'])
df['Country'] = country
df['Street Address'] = street_Address
df['Locality'] = locality
df['Postal Code'] = postal_Code
df['Region'] = region

df.to_csv('university_list.csv')
print(df)
