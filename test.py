import tensorflow as tf
from PIL import Image
import numpy as np

from train import CNN

class Predict(object):
	def __init__(self):
		latest = tf.train.latest_checkpoint('./ckpt')
		self.cnn = CNN()
		self.cnn.model.load_weights(latest)

	def predict(self, image_path):
		img = Image.open(image_path).convent('L')
		img = np.reshape(img, (28, 28, 1)) / 255.
		self.predict_img(img)

	def predict_img(self, image):
		x = np.array([1-image])
		y = self.cnn.model.predict(x)
		predict_result = np.argmax(y[0])
		print('      -> Predict digit', predict_result)
		return predict_result