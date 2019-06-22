from flask import Flask, render_template
import os
import random
from query import query_endpoint
import cv2
import pandas as pd

captcha_source = os.path.join('static', 'data', 'google-10000-english-usa-no-swears-medium.txt')

CAPTCHAS_DIR = os.path.join('static', 'img', 'captchas')

app = Flask(__name__)
n_words = 100


def loadWords(words_path):
    with open(words_path, 'r') as source:
        words_list = [word.replace('\n', '') for word in source.readlines()]
    return words_list


words_list = loadWords(captcha_source)[:n_words]
print("Recognizable words: ", words_list)

def convertImageToJson(path):
    img_width = 160
    img_height = 60
    img_cols = 28 #img_width // 2
    img_rows = 28 #img_height // 2
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    tested_img = cv2.resize(gray, (img_rows, img_cols))
    x_train = tested_img.reshape(img_cols*img_rows)
    x_train = x_train.astype('float32')
    x_train /= 255
    return pd.DataFrame([x_train]).to_json(orient="split")


@app.route('/')
@app.route('/index')
def index():
    number = random.randint(0, 9)
    filename = os.path.join(CAPTCHAS_DIR, '{}.png'.format(number))
    input_json = convertImageToJson(filename)
    results = query_endpoint("captcha", input_json)[0]
    labels, values = get_top(results)
    return render_template("index.html", user_image=filename, labels=labels, values=values)


def get_top(results, n=3):
    labels = sorted(results, key=results.get, reverse=True)[:n]
    values = [results[label] for label in labels]
    print("values: ", values)
    print("labels: ", labels)
    return labels, values


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)