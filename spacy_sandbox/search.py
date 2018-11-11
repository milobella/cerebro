"""
Example use of the spaCy NLP tools for data exploration.
Here we will look for reddit comments that describe Google doing something,
i.e. discuss the company's actions. This is difficult, because other senses of
"Google" now dominate usage of the word in conversation, particularly references to
using Google products.
The heuristics here are quick and dirty --- about 5 minutes work. A better approach
is to use the word vector of the verb. But, the demo here is just to show what's
possible to build up quickly, to start to understand some data.
"""
from __future__ import unicode_literals
from __future__ import print_function
import sys

import plac
import bz2
import ujson
import fr_core_news_sm


def main():
    nlp = fr_core_news_sm.load()  # Load the model takes 10-20 seconds.
    print (nlp)
    # for line in bz2.BZ2File(input_loc):  # Iterate over the reddit comments from the dump.
    #     comment_str = ujson.loads(line)['body']  # Parse the json object, and extract the 'body' attribute.
    #
    #     comment_parse = nlp(comment_str)  # Apply the spaCy NLP pipeline.
    #     for word in comment_parse:  # Look for the cases we want
    #         if google_doing_something(word):
    #             # Print the clause
    #             print(''.join(w.string for w in word.head.subtree).strip())


def google_doing_something(w):
    if w.lower_ != 'google':
        return False
    elif w.dep_ != 'nsubj':  # Is it the subject of a verb?
        return False
    elif w.head.lemma_ == 'be' and w.head.dep_ != 'aux':  # And not 'is'
        return False
    elif w.head.lemma_ in ('say', 'show'):  # Exclude e.g. "Google says..."
        return False
    else:
        return True


if __name__ == '__main__':
    main