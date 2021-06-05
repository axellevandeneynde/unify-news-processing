import flask
from flask import request
from collections import OrderedDict
from nltk.corpus import stopwords
from spacy.lookups import Lookups
from spacy.lemmatizer import Lemmatizer
import json
# https://programmerbackpack.com/automated-python-keywords-extraction-textrank-vs-rake/
from gensim.summarization import keywords
# https://github.com/susanli2016/NLP-with-Python/blob/master/NER_NLTK_Spacy.ipynb

import spacy
print('loading dutch model...')
nlp = spacy.load('nl_core_news_lg')
print('loaded')
stopWordsDutch = set(stopwords.words('dutch'))

# extracts keywords with text-rank algorithm


class TextRank:
    def __init__(self, text):
        self.text = text

    def getKeywords(self):
        return (keywords(self.text).split('\n'))

# Uses spacy pretrained model to exract named entities (NER)


def namedEntityRecognition(text):
    doc = nlp(text)
    return [(X.text, X.label_) for X in doc.ents]


def getDutchArticlesLabels(articles):
    for article in articles:
        text = article['title'] + article['description']
        # ----- get Keywords
        textRank = TextRank(text)
        keywordsText = textRank.getKeywords()[:10]
        # ----- remove dutch stopwords
        filterdKeywords = []
        for word in keywordsText:
            if word not in stopWordsDutch:
                filterdKeywords.append(word)
        # ----- get named entities
        entities = namedEntityRecognition(text)
        filteredEntities = []
        # print(entities)
        for entity in entities:
            if entity[1] != 'CARDINAL' and entity[1] != 'ORDINAL':
                filteredEntities.append(entity[0])

        # TO DO: find a way to lemmatize dutch words!!!!!

        # ------ putting labels together & clean them up
        labels = filterdKeywords + filteredEntities
        lowerCaseLabels = []
        for label in labels:
            lowerCaseLabels.append(label.lower())
        labelsWithoutDuplicates = list(OrderedDict.fromkeys(lowerCaseLabels))
        # ----- add labels to article dict
        article.update({
            'labels': labelsWithoutDuplicates
        })

    return articles


# initialize API
app = flask.Flask(__name__)
app.config["DEBUG"] = True

# ------- Routes

# accepts an array of objects with at least a key 'title' and a key 'description'


@ app.route('/generateDutchLabels', methods=['POST'])
def generateDutchLabels():
    req_data = request.get_json()
    response = json.dumps(getDutchArticlesLabels(req_data))
    return response


app.run(port=5001)
