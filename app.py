
import streamlit as st
import cv2
import numpy as np
import os
import sys
import requests
from PIL import Image

def detect(image):

	# Returning the image with bounding boxes drawn on it (in case of detected objects), and bounding box array
	return image

def about():
	st.write(
		'''
		An assignment that is possible due to the Minor Smart Robot Manufacturing. Due to the corona lockdown the assignment was focused on the machine learning aspect of detecting a bread.
		''')

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

			images = []
			with Image.open(image_file) as img:
				images.append(np.array(img, dtype=np.uint8))
				images = np.array(images)

			if st.button("Process"):
				response = requests.post(os.environ['API_URL'] + '/drbox/predict', json={'image': images.tolist()})
				st.image(image_file, use_column_width=True)
				# st.success("Found {} bread\n".format(len(image)))

	elif choice == "Dataset":
		Dataset()

	elif choice == "About":
		about()

if __name__ == "__main__":
	main()
