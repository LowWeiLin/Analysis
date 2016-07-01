import pyhmeter
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
from itertools import izip


stopwords = stopwords.words('english')

def book():
    return "HarryPotter2.txt"

def analyze():

    words = words_of_book(book())

    x = []
    y = []

    scores = pyhmeter.load_scores("dataset.txt")


    for i in range(0, len(words)-WINDOW_SIZE+1, SLIDING_SIZE):
        text = words[i:i+WINDOW_SIZE]

        content = [w for w in text if w.lower() not in stopwords]

        h = pyhmeter.HMeter(content, scores).happiness_score()

        x.append(i)
        y.append(h)

        # print i, '/', len(words)
        # if i > 2:
        #     break

    # print x
    # print y
    return x, y

def plot(x, y):

    lines = plt.plot(x, y, 'k')
    plt.axis([0, x[-1], min(y), max(y)])
    plt.show()

def words_of_book(book):

    fp = open(book)

    data = fp.read().replace('\n', ' ')
    words = data.split(' ')
    return words

def print_at(i):

    words = words_of_book(book())

    text = words[i:i+WINDOW_SIZE]
    print " ".join(text)

def peaks(xs, ys):
    
    scores = pyhmeter.load_scores("dataset.txt")


    for x, y in izip(xs, ys):

        if y > 5.55:
            
            print_at(x)
            
            print "====================="

LENGTH = len(words_of_book(book()))
WINDOW_SIZE = int(LENGTH / 10)
SLIDING_SIZE = 500

print SLIDING_SIZE

if __name__ == "__main__":
    x,y = analyze()
    plot(x, y)

    #print_at(x[y.index(min(y))])

    #print_at(x[y.index(max(y))])
    peaks(x, y)
