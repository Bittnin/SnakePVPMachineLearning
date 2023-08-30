import tensorflow as tf
from tensorflow import feature_column
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from six.moves import urllib


# Load dataset
dftrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv')  # training data
dfeval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')  # testing data
y_train = dftrain.pop('survived')
y_eval = dfeval.pop('survived')


