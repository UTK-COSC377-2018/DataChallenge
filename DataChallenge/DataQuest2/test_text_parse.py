import json
import nltk
from collections import defaultdict

#Downloads and allows access to 'words' library in nltk module
nltk.download('words')


# Creates a new .json file and writes all json-like objects
# from text file to the new .json file
def create_json(new_line_string):
	with open('aminer_papers_0.json', 'w') as outfile:
		json.dump(new_line_string, outfile)


# Writes each json object from .json file into a list 
def write_json():
	with open('aminer_papers_0.json', 'r') as infile:
		data_string = json.load(infile)
	return data_string


# Parse and extract all titles from each json object
# Function only deals with titles of the English and Spanish
# language. Any foreign papers, such as Chinese or German, 
# are not added to the list to simplify the purpose of this
# program. 
def create_title_list(data_string):
	words = set(nltk.corpus.words.words())
	title_list=[]
	count = 0
	for i in range(len(data_string)):
		if count < 500:
			data = json.loads(data_string[i])
			
			if any('title' in s for s in data):
				title = " ".join(w for w in nltk.wordpunct_tokenize(data['title']) if w.lower() in words and w.isalpha())
				title_list.append(str(title))
				count += 1
		
	return title_list


# Parse and extract all authors from each json object
def create_author_names(data_string):
	author_names=[]
	for i in range(len(data_string)):
		data = json.loads(data_string[i])
		if any('authors' in s for s in data):
			for k in range(len(data['authors'])):
				author_names.append(data['authors'][k]['name'])
	return author_names
	

# Parse and extract all keywords from each json object
def create_keyword_list(data_string):
	keyword_list=[]
	keyword_dict = defaultdict(list)
	for i in range(len(data_string)):
		data = json.loads(data_string[i])
		if any('keywords' in s for s in data):
			for k in range(len(data['keywords'])):
				w = data['keywords'][k]
				if 'title' in data:
					keyword_dict[w].append(data['title'])
	for j in keyword_dict:
		keyword_dict[j].sort()
	keyword_dict =  {k.lower(): v for k, v in keyword_dict.items()}
	return keyword_dict


# Parse and extract all abstracts from each json object
def create_abstract_list(data_string):
	abstract_list=[]
	abs_doc_link = {}
	for i in range(len(data_string)):
		data = json.loads(data_string[i])
		if any('abstract' in s for s in data):
			abstract_list.append(data['abstract'])
			abs_doc_link[i] = data['abstract']
	return abstract_list, abs_doc_list
