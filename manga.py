#! /usr/bin/env env
import sys
import cv2
import numpy as np
from pylab import array, plot, show, axis, arange, figure, uint8 

def sharp(mangaStr):
	manga = str(mangaStr)
	
	#print manga
	img = cv2.imread(manga)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	img = cv2.adaptiveBilateralFilter(img, (5,5),75)

	#sharp
	img = cv2.addWeighted(img, 1.5, img,-0.5,0)
	cv2.imwrite('berserkSarpening.jpg', img)

def contrast(mangaStr):

	manga = str(mangaStr)
	img = cv2.imread(manga)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	maxIntensity = 255.0 
	# depends on dtype of image data
	# Parameters for manipulating image data
	phi = 1
	theta = 1

	# Decrease intensity such that
	# dark pixels become much darker, 
	# bright pixels become slightly dark 
	newImage1 = (maxIntensity/phi)*(img/(maxIntensity/theta))**2
	newImage1 = array(newImage1,dtype=uint8)
	cv2.imwrite('berserkDark.jpg', newImage1)

	newImage0 = (maxIntensity/phi)*(img/(maxIntensity/theta))**0.5
	newImage0 = array(newImage0,dtype=uint8)
	newImage0 = cv2.addWeighted(newImage0, 1.5, img,-0.5,0)
	cv2.imwrite('berserkBrigh.jpg', newImage0)

def dinamicContrast(alpha, beta, mangaStr):

	manga = str(mangaStr)
	img = cv2.imread(manga)

	#contrast
	mul_img = cv2.multiply(img,np.array([alpha]))                    	 # mul_img = img*alpha 
	#brightness
	new_img = cv2.add(mul_img,np.array([beta]))					         # new_img = img*alpha + beta

	cv2.imwrite('original_image.jpg', img)

	img = cv2.adaptiveBilateralFilter(new_img, (5,5),75)
	#sharp
	new_img = cv2.addWeighted(img, 1.5, new_img,-0.5,0)
	cv2.imwrite('new_image.jpg',new_img)

