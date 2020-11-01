import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import cv2

sys.path.append("../src")
print(sys.path)
from ocr.normalization import word_normalization, letter_normalization
from ocr import page, words, characters
from ocr.helpers import implt, resize
from ocr.tfhelpers import Model
from ocr.datahelpers import idx2char


# get_ipython().run_line_magic('matplotlib', 'inline')
plt.rcParams["figure.figsize"] = (15.0, 10.0)

IMG = "../data/ml.png"  # 1, 2, 3
LANG = "en"
# You can use only one of these two
# You HABE TO train the CTC model by yourself using word_classifier_CTC.ipynb
MODEL_LOC_CHARS = "../models/char-clas/" + LANG + "/CharClassifier"


CHARACTER_MODEL = Model(MODEL_LOC_CHARS)


# Crop image and get bounding boxes
image = cv2.cvtColor(cv2.imread(IMG), cv2.COLOR_BGR2RGB)
crop = page.detection(image)
implt(crop)
boxes = words.detection(crop)
lines = words.sort_words(boxes)


# get_ipython().system('pip install textblob')
# get_ipython().system('pip install editdistance')
from textblob import TextBlob
import sys
import argparse
import cv2
import editdistance
from DataLoader import DataLoader, Batch
from Model import Model, DecoderType
from SamplePreprocessor import preprocess


decoderType = DecoderType.BestPath
model = Model(open("..\model\charList.txt").read(), decoderType, mustRestore=True)


# get_ipython().system('pip install pyspellchecker')
# get_ipython().system('pip install indexer')
from spellchecker import SpellChecker

spell = SpellChecker()


def recognise(img):
    """Recognition using character model"""
    # Pre-processing the word
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = preprocess(img, Model.imgSize)
    batch = Batch(None, [img])
    (recognized, probability) = model.inferBatch(batch, True)
    # return str(TextBlob(recognized[0]).correct())
    # return recognized[0]
    return spell.correction(recognized[0])


implt(crop)

text = []
for line in lines:
    text.extend([recognise(crop[y1:y2, x1:x2]) for (x1, y1, x2, y2) in line])


print(" ".join(text))
for idx, word in enumerate(text):
    if (
        word[0].isupper()
        and text[idx - 1] != "."
        and text[idx - 1][-1] != "."
        and idx != 0
    ):
        text.insert(idx, ".")

s = " ".join(text)
with open("../../../ans_ml.txt", "w") as f:
    f.write(s)
