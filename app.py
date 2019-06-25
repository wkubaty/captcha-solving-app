import os
import random

from flask import Flask, render_template, request

from models.captcha import Captcha
from services.generator import Generator
from services.query import Query
from utils.helper import load_words

app = Flask(__name__)

captcha_source = os.path.join('static', 'data', 'google-10000-english-usa-no-swears-medium.txt')
captchas_dir = os.path.join('static', 'img', 'captchas')

n_words = 100
duplicates = 5
words = load_words(captcha_source)[:n_words]
query = Query(words, "captcha", "http://127.0.0.1:1234/invocations")
generator = Generator(captchas_dir, words)
generator.generate_captcha_images(duplicates=duplicates)
print("Recognizable words: ", words)


@app.route('/')
@app.route('/index')
def index():
    word = request.args.get('word', type=str)
    random_word = words[random.randint(0, n_words - 1)]
    random_duplicate = random.randint(0, duplicates - 1)
    if word:
        generator.generate_single_captcha_image(word, random_duplicate)
        random_word = word

    filename = os.path.join(captchas_dir, '{}_{}.png'.format(random_word, random_duplicate))

    captcha = Captcha(filename)
    data_json = captcha.convert_image_to_json()
    # labels, values = query.query_endpoint("captcha", data_json)[0]
    labels, values = query.query_local(data_json)

    return render_template("index.html", words=words, captcha_word=random_word, user_image=filename, labels=labels, values=values)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
