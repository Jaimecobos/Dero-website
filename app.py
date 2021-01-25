
import streamlit as st
import cv2
import numpy as np
import os
import sys
import requests
from PIL import Image

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from visualization import visualize


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
				try:
					response = requests.post(os.environ['API_URL'] + '/drbox/predict', json={'image': images.tolist()}, timeout=3.05)
					if response.status_code == 200:
						detections = np.array(response.json().get('detections'))
						processed_image = visualize(image_file, detections)
						st.pyplot(fig=processed_image)
						# st.success("Found {} bread\n".format(len(image)))
					else:
						st.write("Processing server returned status code {}".format(response.status_code))
				except requests.Timeout:
					st.write("Failed to connect to processing server.")
	elif choice == "Dataset":
		Dataset()

	elif choice == "About":
		about()

if __name__ == "__main__":
	main()
