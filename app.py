from flask import Flask, jsonify
from itertools import permutations
import enchant

app = Flask(__name__)

d = enchant.Dict('es')


def prepare_list(word_):
    new_letters = [word_]
    for i_, letter in enumerate(word_, start=0):
        if letter in 'aeiou':
            new_letter = letter + u'\u0301'
            new_word = word_[:i_] + new_letter + word_[i_ + 1:]
            new_letters.append(new_word)
    return new_letters


def extract_words(word_, size_):
    words = set()
    for p in permutations(word_, size_):
        w = "".join(p)
        if d.check(w):
            words.add(w)
    return words


@app.route('/<letters>', methods=['GET'])
def get_user(letters):
    size = len(letters) + 1
    list_words = prepare_list(letters)

    result = {}
    for i in range(3, size):
        final_list = []
        for word in list_words:
            list_ = extract_words(word, i)
            if len(list_) > 0:
                final_list.extend(list_)
        result[i] = list(set(final_list))
    return jsonify(result)

@app.route('/test')
def test():
    broker = enchant.Broker()
    print(broker.describe())
    return 'test'
