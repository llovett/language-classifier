# classifier.py
#
# A naive Bayes classifier that identifies a given text as being in
# one of English, Spanish, or Romanized Japanese.
# 
# Author: Luke Lovett
# Last Modified: Wed Apr 17 20:38:42 EDT 2013

from sys import argv
from math import log
import os
from pprint import pprint

# Languages
LANGUAGES = ('English','Spanish','Japanese')
# Character information for languages
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
# Count of all documents examined
All_docs_count = 0
# Language document probabilities
P_eng = 0
P_spn = 0
P_jap = 0

def char_index(c):
    return ord(c.lower())-ord('a')

def char_prob(char, lang):
    '''Returns the log probability of the <char> appearing in the <lang>'''
    return log(float(DB[lang][char_index(char)])) - log(float(DB[lang]['all_chars']))

def lang_prob(document, lang):
    '''Returns the log probability of the <document> being in <lang>'''
    return sum( (char_prob(c) for c in document) )

def language(document):
    '''Returns the most likely language for the given <document>'''
    return max((lang_prob(document, lang) for lang in LANGUAGES))
    
def main():
    if len(argv) < 3:
        print "USAGE: python classifier.py <training set dir> <test set dir>"
        exit(1)

    traindir = argv[1]
    testdir = argv[2]

    # Go through each training set file and build knowledge base
    global All_docs_count, P_eng, P_spn, P_jap
    for language in LANGUAGES:
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
                        lang_db['char_counts'][char_index(char)] += 1
                        # Increment all character count for this language
                        lang_db['all_chars'] += 1

    # Set other data
    P_eng = log(DB['English']['document_count']) - log(float(All_docs_count))
    P_spn = log(DB['Spanish']['document_count']) - log(float(All_docs_count))
    P_jap = log(DB['Japanese']['document_count']) - log(float(All_docs_count))

    pprint(DB)

if __name__ == '__main__':
    main()
