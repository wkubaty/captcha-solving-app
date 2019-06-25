import cv2
import numpy as np
import pandas as pd


class Captcha:
    def __init__(self, path):
        self.path = path

    def convert_image_to_json(self):
        img_width = 160
        img_height = 60
        img_cols = img_width // 2
        img_rows = img_height // 2
        img = cv2.imread(self.path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        tested_img = cv2.resize(gray, (img_cols, img_rows))
        x_train = tested_img.reshape(img_cols * img_rows)
        x_train = x_train.astype('float32')
        x_train /= 255
        x_train = np.expand_dims(x_train, axis=0)
        return pd.DataFrame(x_train).to_json(orient="split")
