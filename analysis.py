import pyhmeter
import nltk
import matplotlib.pyplot as plt

def analyze():

    fp = open("HarryPotter.txt")
    data = fp.read()

    words = nltk.word_tokenize(data)

    WINDOW_SIZE = 50
    SLIDING_SIZE = 20

    x = []
    y = []

    scores = pyhmeter.load_scores("dataset.txt")


    for i in range(0, len(words)-WINDOW_SIZE+1, SLIDING_SIZE):
        text = words[i:i+WINDOW_SIZE]

        h = pyhmeter.HMeter(text, scores).happiness_score()

        x.append(i)
        y.append(h)

        print i, '/', len(words)
        # if i > 2:
        #     break

    print x
    print y
    return x, y

def plot(x, y):

    plt.plot(x, y, 'ro')
    plt.axis([0, 6370, 0, 10])
    plt.show()

x,y = analyze()
plot(x, y)


