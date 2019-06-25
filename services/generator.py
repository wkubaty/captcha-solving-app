import os

from captcha.image import ImageCaptcha


class Generator:
    def __init__(self, path, words):
        self.path = path
        self.words = words

    def generate_captcha_images(self, duplicates):
        image = ImageCaptcha(width=160, height=60, font_sizes=[44])
        for word in self.words:
            for i in range(duplicates):
                image.write(word, os.path.join(self.path, '{}_{}.png'.format(word, i)))
