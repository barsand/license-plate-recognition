import cv2
from os import *
import numpy as np
import sys

def preprocess(img):

	height, width = img.shape[:2]
	
	for h in xrange(height):
		count = 0
		for w in xrange(width):

			count += img[h, w]

			if count > 86000:	
				for w in xrange(width):

					img[h, w] = 0


def isLineTooBlack(img, h, width):
	
	count = 0

	for w in xrange(width):
		
		count += img[h,w]

	if count < 25500:
		return True

	else:
		return False



def colourCounter(image):

	height, width = image.shape[:2]

	sections = []

	for h in xrange(0,height-50, 5):

		if not isLineTooBlack(image, h, width):

			for w in xrange(0, width-250, 10):
				
				section = image[h:h+50, w:w+250]

				sections.append((section, h, w))

	plateLocation = (0, 0)
	maxCount = 0

	for s in sections:

		count = 0

		height, width = s[0].shape[:2]

		for h in xrange(height):
			for w in xrange(width):
				
				count += s[0][h, w]

		if count > maxCount:

			maxCount = count
			plateLocation = (s[1], s[2])

			print plateLocation, maxCount

		cv2.imshow('section', s[0])
		cv2.waitKey(1)

	print plateLocation

	cv2.imshow('RESULT', image[plateLocation[0]:plateLocation[0]+50, plateLocation[1]:plateLocation[1]+250])
	cv2.waitKey(5)

	return plateLocation

def markImage(img, height, width):

	for h in xrange(height,height+50):
		
		img[h, width] = [0,0,255]
		img[h, width+1] = [0,0,255]
		img[h, width+2] = [0,0,255]
		img[h, width+3] = [0,0,255]
		img[h, width+250] = [0,0,255]
		img[h, width+251] = [0,0,255]
		img[h, width+252] = [0,0,255]
		img[h, width+254] = [0,0,255]

	for w in xrange(width, width+250):
		
		img[height, w] = [0,0,255]
		img[height+1, w] = [0,0,255]
		img[height+2, w] = [0,0,255]
		img[height+3, w] = [0,0,255]
		img[height+50, w] = [0,0,255]
		img[height+51, w] = [0,0,255]
		img[height+52, w] = [0,0,255]
		img[height+53, w] = [0,0,255]

def main():

	for i in xrange(1,53):

		# read image
		image = cv2.imread(str(i) +'.jpg', cv2.IMREAD_GRAYSCALE)
		colourImage = cv2.imread(str(i) +'.jpg', cv2.IMREAD_COLOR)

		print '*********', i

		# simple binary THRESHOLD
		ret,thresh = cv2.threshold(image,180,255,cv2.THRESH_BINARY)

		# laplacian = cv2.Laplacian(thresh, cv2.CV_64F)
		# laplacian = cv2.Laplacian(image, cv2.CV_64F)

		preprocess(thresh)

		platelocation = colourCounter(thresh)

		markImage(colourImage, platelocation[0], platelocation[1])

		# save image
		# cv2.imwrite(str(i) +'-output.jpg',thresh)
		# cv2.imwrite(str(i) +'-output.jpg',laplacian)
		cv2.imwrite(str(i) +'-output.jpg',colourImage)

		height, width = image.shape[:2]

if __name__ == '__main__':
 	main() 
