from flask import Flask, jsonify, render_template
from itertools import permutations
import enchant
import os

app = Flask(__name__)

# Workaround of: 'a' + u'\u0301' != 'á'
LETTERS_WITH_ACCENTS = {
    'a': 'á',
    'e': 'é',
    'i': 'í',
    'o': 'ó',
    'u': 'ú',
}


def change_letter_at_index(word, letter, index):
    return word[:index] + letter + word[index + 1:]


def prepare_list(word_):
    new_words = [word_]
    for i_, letter in enumerate(word_, start=0):
        if letter in 'aeiou':
            letter_with_accent = LETTERS_WITH_ACCENTS[letter]
            new_word = change_letter_at_index(word_, letter_with_accent, i_)
            new_words.append(new_word)
    return new_words


def extract_words(word_, size_, dict_):
    words = set()
    for p in permutations(word_, size_):
        w = "".join(p)
        if dict_.check(w):
            words.add(w)
    return words


@app.route('/words/<letters>', methods=['GET'])
def get_words(letters):
    # TODO Move this to top level of the file
    d = enchant.Dict('es')

    size = len(letters) + 1
    list_words = prepare_list(letters)

    # TODO Change to proper logger
    print(f'Searching words from: {list_words}')

    result = {}
    for i in range(3, size):
        print(f'Searching words with {i} letters')
        final_list = []
        for word in list_words:
            list_ = extract_words(word, i, d)
            if len(list_) > 0:
                final_list.extend(list_)
        if len(final_list) > 0:
            result[i] = sorted(list(set(final_list)))

    print(f'{len({x for v in result.values() for x in v})} words found')
    return jsonify(result)


@app.route('/config', methods=['GET'])
def config():
    broker = enchant.Broker()
    return {
        'brokers': str(broker.describe()),
        'list_languages': enchant.list_languages(),
        'enchant_config_dir': os.environ.get('ENCHANT_CONFIG_DIR')
    }


@app.route('/', methods=['GET'])
def main():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
