# classifier.py
#
# A naive Bayes classifier that identifies a given text as being in
# one of English, Spanish, or Romanized Japanese.
# 
# Author: Luke Lovett
# Last Modified: Wed Apr 17 20:38:42 EDT 2013

from sys import argv
import os
from pprint import pprint

# Information we need for the classifier
DB = {
    'English':
        {
        'document_count':0,
        'char_counts':[0]*26,
        'all_chars':0
        },
    'Spanish':
        {
        'document_count':0,
        'char_counts':[0]*26,
        'all_chars':0
        },
    'Japanese':
        {
        'document_count':0,
        'char_counts':[0]*26,
        'all_chars':0
        }
}
All_docs_count = 0

def language(document):
    '''Returns the most likely language for the given <document>.'''
    

def main():
    if len(argv) < 3:
        print "USAGE: python classifier.py <training set dir> <test set dir>"
        exit(1)

    traindir = argv[1]
    testdir = argv[2]

    # Convert character to array index
    index = lambda char:ord(char.lower())-ord('a')

    # Go through each training set file and build knowledge base
    global All_docs_count
    for language in ('English','Japanese','Spanish'):
        dirname = os.path.join(traindir,language)
        for ifname in os.listdir(dirname):
            # Increment count for document in current language
            lang_db = DB[language]
            lang_db['document_count'] += 1
            # Increment global document count
            All_docs_count += 1
            with open(os.path.join(dirname,ifname),"r") as inputfile:
                contents = inputfile.read()
                for char in contents:
                    if char.isalpha():
                        # Increment single-character count
                        lang_db['char_counts'][index(char)] += 1
                        # Increment all character count for this language
                        lang_db['all_chars'] += 1

    pprint(DB)

if __name__ == '__main__':
    main()
