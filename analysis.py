import string
from itertools import izip
import re

import pyhmeter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import wordpunct_tokenize
import matplotlib.pyplot as plt
import numpy as np
import cursor as c

_stopwords = stopwords.words('english')


def book():
    return "stories/HarryPotter3.txt"


def scores_dataset():
    return "dataset.txt"

non_alpha_pattern = re.compile('[^a-zA-Z]')

def strip_punctuation(text):
    """
    Naively strip punctuation. 
    Unicode stuff doesn't matter since the sentiment analysis will only match 
    on ascii words anyway.
    """

    return non_alpha_pattern.sub(' ', text)


def words_of_book(book):
    with open(book) as f:
        data = f.read()
    return wordpunct_tokenize(strip_punctuation(data.replace('\n', ' ').lower()))


def paragraphs_of_book(book):
    with open(book) as f:
        data = f.read()
    return [strip_punctuation(para.replace('\n', ' ').lower()) for para in data.split('\n\n')]


def words_of_paragraphs(paragraphs):
    words = []
    for paragraph in paragraphs:
        words.extend(wordpunct_tokenize(paragraph))
    return words


def analyze(window_size, sliding_size, words_or_paragraphs=paragraphs_of_book):
    units = words_or_paragraphs(book())

    x = []
    y = []

    scores = pyhmeter.load_scores(scores_dataset())

    for i in range(0, len(units) - window_size + 1, sliding_size):
        text = units[i:i + window_size]
        paragraph_text = words_of_paragraphs(text)

        # handle stopwords with deltah
        h = pyhmeter.HMeter(paragraph_text, scores, deltah=2.0).happiness_score()

        x.append(i)
        y.append(h)

    return x, y

def gradient(xs, ys):
    new_ys = []
    for i, y in enumerate(ys[1:]):
        new_ys.append(abs(y - ys[i -1]))

    return xs[1:], new_ys

def plot(x, y, onclick):
    fig, ax = plt.subplots()
    cursor = c.SnaptoCursor(ax, x, y)
    plt.connect('motion_notify_event', cursor.mouse_move)
    plt.connect('button_release_event', onclick(cursor))
    ax.plot(x, y, 'k')
    plt.axis([0, x[-1], min(y), max(y)])
    plt.show()


def print_at(i, window_size, words_or_paragraphs=paragraphs_of_book):
    words = words_or_paragraphs(book())

    text = words[i:i + window_size]
    print " ".join(text)


def print_peaks(window_size, xs, ys, words_or_paragraphs=paragraphs_of_book):
    scores = pyhmeter.load_scores(scores_dataset())

    highs = np.percentile(ys, 95)

    print "high is", highs
    for x, y in izip(xs, ys):
        if y > highs:
            print_at(x, window_size, words_or_paragraphs)
            print "====================="

def onclick(window_size, words_or_paragraphs=paragraphs_of_book):
    def why(cursor):
        def handler(event):
            # x, _ = event.xdata, event.ydata
            x, _ = cursor.last_x, cursor.last_y
            print_at(int(x), window_size, words_or_paragraphs)
        return handler
    return why



if __name__ == "__main__":
    split_book = words_of_book

    length = len(split_book(book()))

    window_size = length / 12
    sliding_size = window_size

    print "length", length
    print "window", window_size
    print "slide", sliding_size

    x, y = analyze(window_size, sliding_size, split_book)
    x, y = gradient(x, y)

    print "avg gradient", np.mean(y)

    plot(x, y, onclick(window_size, split_book))

    # print_at(x[y.index(min(y))])

    # print_at(x[y.index(max(y))])
    #print_peaks(window_size, x, y, split_book)
