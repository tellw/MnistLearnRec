from tensorflow.keras import datasets
import cv2
import os

(train_images, train_labels), (test_images, test_labels) = datasets.mnist.load_data(path=os.path.abspath(os.path.dirname(__file__))+'/data_set_tf2/mnist.npz')
for i in range(10):
	print(train_labels[i])
	cv2.imshow('img%d'%i, train_images[i])
	cv2.waitKey()
cv2.destroyAllWindows()