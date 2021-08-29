# Description

This presents a simple set of python codes for image compression using SVD (Singular Value Decomposition).

Coding image compression via SVD is a good practice; one can learn SVD which is such an important concept in linear algebra, and can also get used to handling image data.

---
# SVD (Singular Value Decomposition)

A very brief explanation of SVD is given in the file in [SVD.ipynb](https://github.com/twy80/svd_image/blob/main/SVD.ipynb).

---

# Program files

There are only four program files: 1) one file containing the main SVD and plotting functions, and 2) three independent files doing basically the same things except for the user interface.

1. **svd_image_functions.py**

   - **svd_image** performs the SVD of an image, and compresses it.

   - **plot_images** plots the original and compressed images.

   - **plot_images_tk** plots the original and compressed images on tkinter windows.


2. **svd_image_cmd.py**, **svd_image_entry.py**, and **svd_image_scale.py**

   - [2.1] **svd_image_cmd.py** performs image compression via SVD by using **svd_image** and plots the resulting images using **plot_images**. The input image and the output rank are given from the keyboard.

   - [2.2] **svd_image_entry.py** performs image compression via SVD by using **svd_image** and plots the resulting images using **plot_images_tk** as in 2.1. GUI interface is employed here.

   - [2.3] **svd_image_scale.py** is almost identical to **svd_image_entry.py** except for a slightly different way of selecting the output rank. Instead of an Entry widget as in 2.2, a Scale widget is employed here.

---
# Environment

This code works on python 3.8 and is believed to do so on earlier versions as well. Testing was done both on Windows 10 and mac OS.

---
# Usage

Just run one of the three programs in 2 (Program files).

---
# Feedback

Any comments are welcome!! I was coding in C in the 20th century, and have been using Matlab a lot. I recently started rewriting some of my Matlab programs in python as I may not be able to use (expensive) Matlab after I retire. In view of this, my python codes may not be very pythonic.
