import json
import re
import zhon
from collections import defaultdict

def new_file_json(user_file):
	##user_file = input('Input a file you would like to check.')
	file = open(user_file,"r")
	lines = file.readlines()
	file.close()

	line_string = []
	for line in lines:
		line = line.strip()
		line_string.append(line)

	return line_string

def create_json(new_line_string):
	with open('aminer_papers_0.json', 'w') as outfile:
		json.dump(new_line_string, outfile)

def write_json():
	with open('aminer_papers_0.json', 'r') as infile:
		data_string = json.load(infile)
	return data_string

def create_title_list(data_string):
	title_list=[]
	count = 0
	for i in range(len(data_string)):
		if count < 250:
			data = json.loads(data_string[i])
			if any('title' in s for s in data):
			#chinese_text = re.findall('[%s]' % zhon.unicode.HAN_IDEOGRAPHS, data['title'])			
			#if chinese_text == 0:
				title_list.append(str(data['title']))
		count += 1
		
	return title_list

def create_title_dict(data_string):
	title_dict={}
	title_key = []
	count = 0
	for i in range(len(data_string)):
		if count != 250:
			data = json.loads(data_string[i])
			if any('title' in s for s in data):
				if any('keywords' in s for s in data):
					for k in range(len(data['keywords'])):
						title_key.append(data['keywords'])
					title_dict[data['title']] = ' '.join(title_key[0])
					count += 1
		
	return title_dict

def create_author_names(data_string):
	author_names=[]
	for i in range(len(data_string)):
		data = json.loads(data_string[i])
		if any('authors' in s for s in data):
			for k in range(len(data['authors'])):
				author_names.append(data['authors'][k]['name'])
	return author_names
	
def create_author_freq(names_list):
	author_freq = {}
	for names in names_list:
		if names in author_freq:
			author_freq[names] += 1
		else:
			author_freq[names] = 1
	return author_freq

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
	return keyword_dict

def create_keyword_freq(keyword_list):
	keyword_freq = {}
	for words in keyword_list:
		if words in keyword_freq:
			keyword_freq[words] += 1
		else:
			keyword_freq[words] = 1
	return keyword_freq

def create_abstract_list(data_string):
	abstract_list=[]
	abs_doc_link = {}
	for i in range(len(data_string)):
		data = json.loads(data_string[i])
		if any('abstract' in s for s in data):
			abstract_list.append(data['abstract'])
			abs_doc_link[i] = data['abstract']
	return abstract_list, abs_doc_list
