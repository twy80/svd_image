"""
Functions for Image Compression using SVD
Coded by T.-W. Yoon, Aug. 2021
"""

import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from skimage.util import img_as_float, img_as_ubyte


def svd_image(input_image, output_rank, new_image=True):
    """
    This function performs the SVD of an image, and compresses it.

    :param input_image: 2 or 3 dimensional image matrix
    :param output_rank: rank of the compressed image
    :param new_image:   True  => computing the SVD of the image
                        False => reusing the SVD previously computed
    :return:            2 or 3 dimensional compressed image matrix
    """

    input_image = img_as_float(input_image)
    image_shape = input_image.shape

    if len(image_shape) == 2:  # 2-dimensional grayscale images are reshaped to be
        image_shape = (*image_shape, 1)  # 3-dimensional images with a single color
        input_image = input_image.reshape(*image_shape)

    output_image = np.zeros(image_shape)
    rows, columns, channels = image_shape

    if new_image is True:  # Compute SVD for a new image
        ns = min(rows, columns)  # Upper bound on the rank of input image

        svd_image.u = np.zeros((rows, ns, channels))
        svd_image.vt = np.zeros((ns, columns, channels))
        svd_image.s = np.zeros((ns, channels))

        for i in range(channels):  # SVD of each channel
            svd_image.u[:, :, i], svd_image.s[:, i], svd_image.vt[:, :, i] = \
                np.linalg.svd(input_image[:, :, i], full_matrices=False)

    for i in range(channels):  # Compress the image using SVD
        try:  # See if the SVD results previously obtained can be reused
            output_image[:, :, i] = (
                svd_image.u[:, :output_rank, i] * svd_image.s[:output_rank, i]
            ) @ svd_image.vt[:output_rank, :, i]
        except Exception:
            raise Exception(
                "\nProblems with the SVD results previously obtained. Set new_image = True!\n"
            )

        if channels == 1:  # grayscale images are reshaped back to be 2-dimensional images
            output_image = output_image.reshape(rows, columns)

    return img_as_ubyte(np.clip(output_image, 0, 1))


def plot_images(images, descriptions=None):
    """
    This function plots a list of images.

    :param images:          list of images to be plotted
    :param descriptions:    list of captions for the images
    """

    plt.rcParams.update({'font.size': 5})
    num_of_images = len(images)

    plt.close('all')
    fig, axes = plt.subplots(
        1, num_of_images, figsize=(2 * num_of_images, 2), dpi=200
    )
    fig.tight_layout(rect=(0.04, 0.04, 0.96, 0.96))

    for n in range(num_of_images):
        ax = axes[n] if num_of_images > 1 else axes
        ax.imshow(images[n], cmap="gray")
        if descriptions:
            ax.set_title(descriptions[n])
        ax.axis("off")

    plt.show(block=False)
    plt.pause(0.1)


def plot_images_tk(images, descriptions, parent_win, new_window=True):
    """
    This function plots a list of images.

    :param images:          list of images to be plotted
    :param descriptions:    list of captions for the images
    :param parent_win:      Parent tkinter window
    :param new_window:      True  => opening a new window for plotting images
                            False => reusing the window previously prepared
    """

    plt.rcParams.update({'font.size': 5})
    num_of_images = len(images)

    fig = plt.Figure(figsize=(2 * num_of_images, 2), dpi=200)

    for n in range(num_of_images):
        ax = fig.add_subplot(1, num_of_images, n+1)
        ax.imshow(images[n], cmap="gray")
        if descriptions:
            ax.set_title(descriptions[n])
        ax.axis("off")

    if new_window is True:
        plot_images_tk.sub_win = tk.Toplevel(parent_win)
        plot_images_tk.canvas = FigureCanvasTkAgg(fig, master=plot_images_tk.sub_win)
    else:
        plot_images_tk.canvas.get_tk_widget().pack_forget()
        try:
            plot_images_tk.canvas = FigureCanvasTkAgg(fig, master=plot_images_tk.sub_win)
        except Exception:
            plot_images_tk.sub_win = tk.Toplevel(parent_win)
            plot_images_tk.canvas = FigureCanvasTkAgg(fig, master=plot_images_tk.sub_win)

    plot_images_tk.canvas.draw()
    plot_images_tk.canvas.get_tk_widget().pack()
    fig.tight_layout(rect=(0.04, 0.04, 0.96, 0.96))
