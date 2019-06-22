from flask import Flask, render_template
import os
import random

CAPTCHAS_DIR = os.path.join('static', 'img', 'captchas')

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def show_index():
    number = random.randint(0, 9)
    filename = os.path.join(CAPTCHAS_DIR, 'about_{}.png'.format(number))
    labels = ["about", "black", "chance"]
    values = [0.9, 0.08, 0.02]
    return render_template("index.html", user_image=filename, labels=labels, values=values)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
