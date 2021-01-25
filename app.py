
import streamlit as st
import cv2
import numpy as np
import os
import sys
import requests
from PIL import Image
import matplotlib.pyplot as plt


def visualize(image, pred_labels):
    '''
    Visualization tool to plot images with ground truth boxes and/or predicted labels

    Arguments:
        image (numpy array) : the image to plot
        gt_labels (np array, optional) : the ground truth labels, this will be plot in red
        pred_labels (np array, optional) : the predicted labels, this will be plot in blue
        save_folder (string, optional) : if set, the image is not plot but saved with this path

    '''

    plt.figure(figsize=(12, 12))
    plt.imshow(image)
    current_axis = plt.gca()

    current_axis.text(1, -10, '- Predicted boxes bread roll top', size='x-large', color='green', bbox={'facecolor': 'white', 'alpha': 1.0})
    current_axis.text(150, -10, '- Predicted boxes bread roll bottom', size='x-large', color='red', bbox={'facecolor': 'white', 'alpha': 1.0})

    for box in pred_labels:
        class_id = box[0]
        cx = box[2]
        cy = box[3]
        w = box[4]
        h = box[5]
        angle = box[6]

        xmin, ymin = cx - 1 / 2 * (-h * np.sin(angle) + w * np.cos(angle)), \
                     cy - 1 / 2 * (h * np.cos(angle) + w * np.sin(angle))

        if class_id == 1:
            color = 'green'
        else:
            color = 'red'

        current_axis.add_patch(
            plt.Rectangle((xmin, ymin), w, h, angle=angle * 180 / np.pi, color=color, fill=False, linewidth=2))

        label = '{:.2f}'.format(box[1])
        current_axis.text(xmin, ymin, label, size='x-small', color='black', bbox={'facecolor': color, 'alpha': 1.0})

    return plt.gcf()


def about():
	st.write(
		'''
		An assignment that is possible due to the Minor Smart Robot Manufacturing. Due to the corona lockdown the assignment was focused on the machine learning aspect of detecting a bread.
		''')


def main():
	st.title("Bread Detection App :Bread: ")
	st.write("**Rotated Bounding Box detection using Keras and TensorFlow**")

	activities = ["Home", "About"]
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
						processed_image = visualize(images[0], detections)
						st.pyplot(fig=processed_image)
					else:
						st.write("Processing server returned status code {}".format(response.status_code))
				except requests.Timeout:
					st.write("Failed to connect to processing server.")
	elif choice == "About":
		about()


if __name__ == "__main__":
	main()
