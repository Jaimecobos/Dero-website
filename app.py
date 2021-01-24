
import streamlit as st
import cv2
import pandas as pd
import numpy as np
import os
import sys
from PIL import Image
from io import BytesIO,StringIO

def detect(image):

	# Returning the image with bounding boxes drawn on it (in case of detected objects), and bounding box array
	return image

def about():
	st.write(
		'''
		An assignment that is possible due to the Minor Smart Robot Manufacturing. Due to the corona lockdown the assignment was focused on the machine learning aspect of detecting a bread.
		''')

def load_image(image_file):
	img = Image.open(image_file)
	return img

def main():
	st.title("Bread Detection App :Bread: ")
	st.write("**Bounding box detection using keras and tenserflow**")

	activities = ["Home", "Dataset", "About"]
	choice = st.sidebar.selectbox("Pick something", activities)

	if choice == "Home":
		st.write("Go to the About section from the sidebar to learn more about it.")

		# Specify the files types.
		image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])
		if image_file is not None:
			image = Image.open(image_file)

			if st.button("Process"):
				image = load_image(image_file)
				st.image(image, use_column_width = True)
				st.success("Found {} bread\n".format(len(image)))

	elif choice == "About":
		about()

if __name__ == "__main__":
	main()
