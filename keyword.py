### Keyword Frequency Script
import os, io
import argparse
import collections
import pandas as pd
from nltk.util import ngrams
import json
import spacy

pos = ['PROPN','NOUN', 'VERB']
stop_words = []

json_keywords = {}
statement = ""

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", type=str, default="-", help="did not specify file")
parser.add_argument("-o", "--output", type=str, default="-", help="did not specify file")

args = parser.parse_args()


if args.file != "-":
    data = pd.read_csv(args.file)
    for i in range(len(data['Tweet'])):
        statement += str(data['Tweet'][i].lower()) + str(". ")

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(statement)
    # unigrams
    words = [token.lemma_ for token in doc if ((not token.is_punct) and (not token.is_stop) and (token.pos_ in pos) and (token.shape_ != "x") and (token.shape_ != "xx") and (token.shape_ != "xxx") and (not token.like_num) and (not token.is_space) )]
    unigrams_n = collections.Counter(words)

    # bigrams
    n_gram = 2
    bigrams_n = collections.Counter(ngrams(words, n_gram))

    unigrams_n = list(filter(lambda x: (x[1] > 10), unigrams_n.most_common()[:50]))
    bigrams_n = list(filter(lambda x: (x[1] > 5), bigrams_n.most_common()[:50]))
    bigrams_n = [(str(k[0][0]) + " " + str(k[0][1]), k[1]) for k in bigrams_n]

    df = pd.DataFrame({'unigrams(NOUN)': pd.Series(unigrams_n), 'bigrams(NOUN)': pd.Series(bigrams_n) })
    df.to_excel(args.output + '/keywords.xlsx', index=False, encoding='utf-8')

    json_keywords['unigrams_n'] = unigrams_n
    json_keywords['bigrams_n'] = bigrams_n

    with open(args.output + "/keywords.json", 'w', encoding='utf-8') as fp:
        json.dump(json_keywords, fp, ensure_ascii=False)
else:
    print("did not specify file")
