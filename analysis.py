import pyhmeter
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import numpy as np
import cursor as c

from itertools import izip

_stopwords = stopwords.words('english')


def book():
    return "sabriel.txt"


def scores_dataset():
    return "dataset.txt"


def words_of_book(book):
    with open(book) as f:
        data = f.read()
    return data.replace('\n', ' ').split(' ')


def paragraphs_of_book(book):
    with open(book) as f:
        data = f.read()
    return [para.replace('\n', ' ') for para in data.split('\n\n')]


def words_of_paragraphs(paragraphs):
    words = []
    for paragraph in paragraphs:
        words.extend(paragraph.split())
    return words


def analyze(window_size, sliding_size, words_or_paragraphs=paragraphs_of_book):
    units = words_or_paragraphs(book())

    x = []
    y = []

    scores = pyhmeter.load_scores(scores_dataset())

    for i in range(0, len(units) - window_size + 1, sliding_size):
        text = units[i:i + window_size]
        paragraph_text = words_of_paragraphs(text)

        content = [w for w in paragraph_text if w.lower() not in _stopwords]

        h = pyhmeter.HMeter(content, scores).happiness_score()

        x.append(i)
        y.append(h)

    return x, y


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

    window_size = int(length / 10)
    sliding_size = window_size / 5

    print "length", length
    print "window", window_size
    print "slide", sliding_size

    x, y = analyze(window_size, sliding_size, split_book)
    plot(x, y, onclick(window_size, split_book))

    # print_at(x[y.index(min(y))])

    # print_at(x[y.index(max(y))])
    print_peaks(window_size, x, y, split_book)
