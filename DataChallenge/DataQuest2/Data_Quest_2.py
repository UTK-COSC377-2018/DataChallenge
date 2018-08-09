import re
import test_text_parse
import test_nltk

#git add DataQuest2
#git commit -m "adds my code for Data Challenge Question 2 to the repo"
#git push origin jdunkley

# Calls write_json() function to write json data into the list data_string
data_string = test_text_parse.write_json()

# Function returns a dictionary of all the titles and their associated keywords 
# from the aminer_papers_0 json objects
title_list = test_text_parse.create_title_list(data_string)


#Delete possible duplicate titles in the list
final_list = []
for i in title_list:
	if i not in final_list:
		final_list.append(i)

test_nltk.cluster_doc(title_list)

	





