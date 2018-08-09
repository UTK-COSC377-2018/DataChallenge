import re
import test_text_parse
import test_nltk

##test_string = test_text_parse.new_file_json("aminer_papers_0.txt")
##test_text_parse.create_json(test_string)
##with open('aminer_papers_0.json') as f:
	##data = json.load(f)

data_string = test_text_parse.write_json()


#keyword_dict = test_text_parse.create_keyword_list(data_string)
#keyword_dict =  {k.lower(): v for k, v in keyword_dict.items()}

# Function returns a dictionary of all the titles and their associated keywords 
# from the aminer_papers_0 json objects
title_dict = test_text_parse.create_title_dict(data_string)
'''
final_list = []
for i in title_list:
	if i not in final_list:
		#j = re.sub(r'\d+', '', i)
		final_list.append(i)
'''
print(title_dict)
#test_nltk.cluster_doc(final_list)

'''
# Loop in which the user enters a specified keyword and the program returns the titles
# of the json objects associated with that word. If keyword does not exist, user is 
# prompted to enter another keyword until he or she exits the program
while True:
	word = input('\nPlease enter in a keyword or press Enter to exit: \n')
	word = word.lower()
	if word in keyword_dict:
		print()
		count = 0
		if len(keyword_dict[word]) > 20:
			n = len(keyword_dict[word])
			for i in range(n):
				if i == 0:
					print(keyword_dict[word][i])
				elif i < 20:
					if i % 19 != 0:
						print(keyword_dict[word][i])
				else:
					if i % 20 == 0:
						print()
						option = input('Would you like to view the next 20 options? \n\n')
						print()
						if option not in ['y', 'ye', 'yes', 'yea', 'yeah']:
							break
				print(keyword_dict[word][i])
						
		else:
			n = len(keyword_dict[word])
			for i in range(n):
				print(keyword_dict[word][i])
	if word == "":
		break
	if word not in keyword_dict:
		continue
'''	





