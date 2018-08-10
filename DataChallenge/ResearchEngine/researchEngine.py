#!/usr/bin/env python3

# Names: Bentley Beard, Ian Lumsden, Hayden Coffey, Michael O'Neil, Joshua Dunkley
# Project for CS 377
# Description: Research Engine creates a search engine that allows the user to navigate the plethora
# of research papers part of the ORNL database. It does so by letting the user enter in 'keywords'
# which are then compared to a python dictionary. If there are keys that match that word, then the
# list of all matches is printed to the screen. If there are no matches, then the program suggests
# keywords that would prompt a match. The user then has the option to enter a title of one
# of the 20 listed papers to recieve more information about the paper. The user can also return to
# search mode to search more subjects.

import sys
import json
import re

# class for storing info about the papers
class Paper:
    def __init__(self, id, title, authors, url, abstract, keywords, fos):
        self.id = id
        self.title = title
        self.url = url
        self.abstract = abstract

        # Extract only name of author and ignore organization
        self.authors = []
        for a in authors:
            if 'name' in a:
                self.authors.append(a['name'])


        # Set up the popularity of each keyword
        self.popularity = {}
        for k in keywords:
            self.popularity[k] = 1
        for f in fos:
            self.popularity[f] = 1

        # Set up the paper to have a set popularity associated with each keyword based on the title and abstract
        re.sub('(?<=\w)([!?,\\-"\';:()])', r' /1', title)
        wordsInTitle = title.split()
        for word in wordsInTitle:
            word = word.lower()
            for key in self.popularity:
                if key in word:
                    self.popularity[key] += 5
        re.sub('(?<=\w)([!?,\\-"\';:()])', r' /1', abstract)
        wordsInAbstract = abstract.split()
        for word in wordsInAbstract:
            word = word.lower()
            for key in self.popularity:
                if key in word:
                    self.popularity[key] += 1

# Adds a paper to the dictionary
def updateDict(subjects, line):
    obj = json.loads(line)
    try:
        lang = obj['lang']
        if lang != 'en':
            return
    except:
        return
    # Get keywords
    try:
        keywords = obj['keywords']
    except:
        keywords = []
    # Get fos
    try:
        fos = obj['fos']
    except:
        fos = []
    # Get id
    try:
        id = obj['id']
    except:
        id = 'n/a'
        print('id not found for paper', num)
    # Get title
    try:
        title = obj['title']
    except:
        title = 'n/a'
        print('title not found for paper', num)
    # Get Author
    try:
        author = obj['authors']
    except:
        author = 'n/a'
    # Get url
    try:
        url = obj['url']
    except:
        url = 'n/a'
    # Get abstract
    try:
        abstract = obj['abstract']
    except:
        abstract = 'n/a'

    # Clean up keywords
    keywords = cleanUp(keywords)
    fos = cleanUp(fos)

    # Initialize paper and store in dict
    paper = Paper(id, title, author, url, abstract, keywords, fos)
    for kw in keywords:
        try:
            if paper not in subjects[kw]:
                subjects[kw].append(paper)
        except:
            subjects[kw] = [paper]
    for sub in fos:
        try:
            if paper not in subjects[sub]:
                subjects[sub].append(paper)
        except:
            subjects[sub] = [paper]
    return

# Ensures that every string in the list is only one word
def cleanUp(sortedPapers):
    rv = []

    for obj in sortedPapers:
        obj = obj.split()
        for word in obj:
            rv.append(word.lower())

    return rv

# Finds common elements between lists
def commonElements(listA, listB):
    setA = set(listA)
    setB = set(listB)
    return list(setA & setB)

# Prints 20 papers
def print20(sortedPapers):
    keyword = 'n'
    loc = 0
    papers = []

    while(keyword != 'search'):
        # Print next 20
        if keyword == 'n':
            print()
            papers = []
            # Standard print 20
            if len(sortedPapers) - loc > 20:
                print('Papers (%d - %d of %d)' % (loc, loc+20, len(sortedPapers)))
                print('----------------------------------------------------------------')
                for i in range(loc, loc+20):
                    print(sortedPapers[i][1].title)
                    papers.append(sortedPapers[i][1])
                loc += 20
            # < 20 print
            else:
                print('Papers (%d - %d of %d)' % (loc, len(sortedPapers), len(sortedPapers)))
                print('----------------------------------------------------------------')
                for i in range(loc, len(sortedPapers)):
                    print(sortedPapers[i][1].title)
                    papers.append(sortedPapers[i][1])
                print('----------------------------------------------------------------')
                print('End of results')
        # Print previous 20
        elif keyword == 'p':
            papers = []
            print()
            loc -= 20
            # Standard print 20
            if(loc >= 20):
                print('Papers (%d - %d of %d)' % (loc-20, loc, len(sortedPapers)))
                print('----------------------------------------------------------------')
                for i in range(loc-20, loc):
                    print(sortedPapers[i][1].title)
                    papers.append(sortedPapers[i][1])
            else:
                # Total list < 20
                if len(sortedPapers) < 20:
                    print('Papers (%d - %d of %d)' % (0, len(sortedPapers), len(sortedPapers)))
                    print('----------------------------------------------------------------')
                    for i in range(0, len(sortedPapers)):
                        print(sortedPapers[i][1].title)
                        papers.append(sortedPapers[i][1])
                # Beginning of list
                else:
                    print('Papers (%d - %d of %d)' % (0, 20, len(sortedPapers)))
                    print('----------------------------------------------------------------')
                    for i in range(0, 20):
                        print(sortedPapers[i][1].title)
                        papers.append(sortedPapers[i][1])
                print('----------------------------------------------------------------')
                print("Beginning of results")
        # List current papers
        elif keyword == 'l':
            print()
            print('Papers (%d - %d of %d)' % (loc-len(papers), loc, len(sortedPapers)))
            print('----------------------------------------------------------------')
            for p in papers:
                print(p.title)
        # exit keyword
        elif(keyword == 'exit'):
            exit(0)
        # check titles
        else:
            print()
            print('----------------------------------------------------------------')
            if(not checkTitles(papers, keyword)):
                print('No papers match your search')
        print('----------------------------------------------------------------')
        print()
        print('Type "n" for next 20, "p" for previous 20, "l" for a list of the current papers, a title for one of the current papers, or search another term')
        keyword = input('In paper mode (type "search" to return to search mode or "exit" to end): ').lower()

    keyword = input('Search (type "exit" to end): ').lower()
    return keyword

# sort the papers based on the "popularity" of the paper
def popSort(papers, searchWords):
    rv = []
    for p in papers:
        pop = 0
        for sw in searchWords:
            if sw in p.popularity:
                pop += p.popularity[sw]
        rv.append([pop, p])
    rv = sorted(rv, key=getKey, reverse=True)

    return rv

# helper fxn for popSort
def getKey(item):
    return item[0]

# Check to see if the user input is one of the 20 papers in 'papers'
def checkTitles(papers, keyword):
    for p in papers:
        if keyword == p.title.lower():
            print('Title:', p.title)
            print('Authors:', end=' ')
            for a in range(0, len(p.authors)-1):
                print(p.authors[a], end=', ')
            print(p.authors[len(p.authors) - 1])
            print()
            print('Abstract:', p.abstract)
            print()
            print("URL's:")
            for url in p.url:
                print('        %s' % url)
            return True
    return False

def main():
    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print('Usage: relatedTopics.py inputFile')
        print('Usage: researchEngine.py inputFile numPapers')
        exit(0)
    num = 0
    subs = []
    subjects= {}

    # Check to see the number of papers to read in (default is 75000)
    if len(sys.argv) == 3:
        iterations = int(sys.argv[2])
    else:
        iterations = 75000

    # Open file to read JSON file
    filename = sys.argv[1]
    with open(filename, 'r') as f:
        for line in f:
            print(num)
            num += 1
            if num > iterations:
                break
            updateDict(subjects, line)

    # Take input from user and begin while loop
    keyword = input('Search (type "exit" to end): ').lower()
    while(keyword != 'exit'):

        keyword = keyword.split()
        allValidPapers = []
        # Check to make sure the user entered at least one keyword (i.e. didn't just hit enter)
        if len(keyword) > 0:
            # allValidPapers can only be initialized after a successful try
            firstSuccess = True
            for i in range(0, len(keyword)):
                try:
                    papers = subjects[keyword[i]]
                except:
                    print()
                    print('----------------------------------------------------------------')
                    print('No results include the word "' + keyword[i] + '"')
                    print('----------------------------------------------------------------')
                    continue
                if firstSuccess == True:
                    allValidPapers = papers
                    firstSuccess = False
                else:
                    allValidPapers = commonElements(allValidPapers, papers)

            # Check to see if any papers were found
            if len(allValidPapers) == 0:
                print()
                print('----------------------------------------------------------------')
                print('No results found. Try some of the following words:')
                print('----------------------------------------------------------------')
                for key in subjects:
                    for word in keyword:
                        if word in key:
                            print(key)
                print('----------------------------------------------------------------')
                print()
                keyword = input('Search (type "exit" to end): ').lower()
            else:
                allValidPapers = popSort(allValidPapers, keyword)
                keyword = print20(allValidPapers)
        else:
            print()
            print('----------------------------------------------------------------')
            print('Error: no keyword entered')
            print('----------------------------------------------------------------')
            print()
            keyword = input('Search (type "exit" to end): ').lower()

if __name__ == '__main__':
    exit(main())
