from analysis import *

def gradient(xs, ys):
    new_ys = []
    for i, y in enumerate(ys[3:]):
        new_ys.append((1.5 * abs(y - ys[i - 1]) + abs(y - ys[i - 2]) + 0.5 * abs(y - ys[i - 3])) / 3.0)

    return xs[3:], new_ys


if __name__ == "__main__":
    split_book = words_of_book

    length = len(split_book(book()))

    window_size = length / 25
    sliding_size = window_size

    print "length", length
    print "window", window_size
    print "slide", sliding_size

    x, y = gradient(*analyze(window_size, sliding_size, split_book))
    

    print "avg gradient", np.mean(y)

    plot(x, y, onclick(window_size, split_book))
