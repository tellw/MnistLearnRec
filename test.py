import tensorflow as tf
from PIL import Image
import numpy as np

from train import CNN
from train import DataSource

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
		# 输入是黑底白字图片
		# x = np.array([1-image])
		# 输入是白底黑字图片
		x = np.array([image])
		y = self.cnn.model.predict(x)
		predict_result = np.argmax(y[0])
		print('      -> Predict digit', predict_result)
		return predict_result

if __name__ == '__main__':
	pass