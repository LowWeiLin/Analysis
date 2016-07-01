import pyhmeter
import nltk
import matplotlib.pyplot as plt

WINDOW_SIZE = 1500
SLIDING_SIZE = 200

def analyze():

    fp = open("HarryPotter.txt")
    data = fp.read()

    words = nltk.word_tokenize(data)


    x = []
    y = []

    scores = pyhmeter.load_scores("dataset.txt")


    for i in range(0, len(words)-WINDOW_SIZE+1, SLIDING_SIZE):
        text = words[i:i+WINDOW_SIZE]

        h = pyhmeter.HMeter(text, scores).happiness_score()

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

def print_at(i):

    fp = open("HarryPotter.txt")
    data = fp.read()

    words = nltk.word_tokenize(data)

    text = words[i:i+WINDOW_SIZE]
    print " ".join(text)

x,y = analyze()
plot(x, y)

#print_at(x[y.index(min(y))])

print_at(x[y.index(max(y))])
