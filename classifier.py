# classifier.py
#
# A naive Bayes classifier that identifies a given text as being in
# one of English, Spanish, or Romanized Japanese.
# 
# Author: Luke Lovett
# Last Modified: Wed Apr 17 23:09:10 EDT 2013

from sys import argv
from math import log, exp
import os, string

# Languages
LANGUAGES = ('English','Spanish','Japanese')
# Character information for languages
DB = {
    'English':
        {
        'document_count':0,
        'char_counts':[0]*len(string.lowercase),
        'all_chars':0,
        'lang_prob':0
        },
    'Spanish':
        {
        'document_count':0,
        'char_counts':[0]*len(string.lowercase),
        'all_chars':0,
        'lang_prob':0
        },
    'Japanese':
        {
        'document_count':0,
        'char_counts':[0]*len(string.lowercase),
        'all_chars':0,
        'lang_prob':0
        }
}
# Count of all documents examined
All_docs_count = 0

def char_index(c):
    return ord(c.lower())-ord('a')

def char_prob(char, lang):
    '''Returns the log probability of the <char> appearing in the <lang>'''
    # Handle special case of char never appearing in the language
    lang_db = DB[lang]
    if lang_db['char_counts'][char_index(char)] == 0:
        return float('-inf')
    return (log(float(DB[lang]['char_counts'][char_index(char)])) -
            log(float(DB[lang]['all_chars'])))

def lang_prob(document, lang):
    '''Returns the log probability of the <document> being in <lang>'''
    return (sum( (char_prob(c,lang) for c in document if c.isalpha()) ) +
            DB[lang]['lang_prob'])

def guess_language(document):
    '''Returns the most likely language for the given <document>'''
    language_probabilities = [(l,lang_prob(document,l)) for l in LANGUAGES]
    return reduce(lambda x,y:x if x[1]>y[1] else y, language_probabilities)[0]

def main():
    if len(argv) < 3:
        print "USAGE: python classifier.py <training set dir> <test set dir>"
        exit(1)

    traindir = argv[1]
    testdir = argv[2]

    #########
    # TRAIN #
    #########

    global All_docs_count
    for language in LANGUAGES:
        dirname = os.path.join(traindir,language)
        lang_db = DB[language]
        for ifname in os.listdir(dirname):
            # Increment count for document in current language
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

    for language in LANGUAGES:
        lang_db = DB[language]
        lang_db['lang_prob'] = log(lang_db['document_count'])-log(float(All_docs_count))

    #################
    # PRINT RESULTS #
    #################

    # Language probabilities, character probabilities
    for language in LANGUAGES:
        lang_db = DB[language]
        print "#"
        print "# {}".format(language.upper())
        print "#"
        print "Probability: {}".format(exp(lang_db['lang_prob']))
        print "Character probabilities:"
        for c in string.lowercase:
            print "{:>5} {}".format(c, exp(char_prob(c,language)))

    # Print the "confusion matrix"
    confusion = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
    # Iterate column, language
    for i,lang in enumerate(LANGUAGES):
        dirname = os.path.join(testdir,lang)
        # Language guesses for language test set
        guesses = []
        for ifname in os.listdir(dirname):
            with open(os.path.join(dirname,ifname),"r") as inputfile:
                guesses.append(guess_language(inputfile.read()))
        # Store guess information in confusion matrix
        for j,lang_guess in enumerate(LANGUAGES):
            confusion[j][i] = len([g for g in guesses if g == lang_guess])

    # Row header
    print "#"
    print "# CONFUSION MATRIX"
    print "#"
    print 10*" ",
    print ("{:>10}"*len(LANGUAGES)).format(*[l.upper() for l in LANGUAGES])
    # Print each entry
    for row,lang in enumerate(LANGUAGES):
        print "{:>8}".format(lang.upper()),
        for col in confusion[row]:
            print "{:>10}".format(col),
        print
    
if __name__ == '__main__':
    main()
