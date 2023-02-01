"""
Image Compression using SVD by T.-W. Yoon, Aug. 2021
"""


def run_svd_image_scale():
    """
    This program performs SVD of an image matrix, compresses it by reducing the rank,
    and uses the following functions:

    plot_images_tk: plotting images on tkinter windows
    select_images:  selecting an image file and computing its rank
    plot_all_reset: plotting all the results and initializing variables & widgets
    check_call_svd: checking the setup and calling the main function
    svd_image:      compressing the image by SVD, the main function.

    plot_images_tk and svd_image are imported from svd_image_functions.py.
    """

    import tkinter as tk
    from tkinter import messagebox

    from svd_image_functions import plot_images_tk, svd_image

    results, captions = [], []
    input_image_int = None
    new_image = True
    rank = 1  # Nonlocal variables shared by functions

    def select_image():
        """
        This function selects an image file and computes its rank.

        The resulting image and rank value are stored
        as nonlocal variables 'input_image_int' and 'rank'.
        """

        import tkinter.filedialog as fd

        import imageio.v3 as iio
        import numpy as np

        nonlocal input_image_int, rank

        image_file_name = fd.askopenfilename(
            title='Select a file!',
            filetypes=[('image files', '.bmp .jpg .jpeg .png .gif'), ('all files', '*')]
        )

        try:
            input_image_int = iio.imread(image_file_name)
        except (SyntaxError, ValueError):
            messagebox.showinfo("Info", "Give a valid image file!")
        else:
            image_shape = input_image_int.shape

            channels = 1 if len(image_shape) == 2 else 3
            # If the image is grayscale, channels = 1

            for i in range(channels):  # Compute the rank of each channel
                if channels == 1:
                    rank = np.linalg.matrix_rank(input_image_int)
                else:
                    rank = max(rank, np.linalg.matrix_rank(input_image_int[:, :, i]))

            button_selection.config(text=f"{image_shape[0]}x{image_shape[1]} image (rank = {rank})")
            scale_rank.config(to=rank, tickinterval=rank-1)  # Put the resulting information on the widgets

    def plot_all_reset():
        """
        This function plots all the results, and initializes the nonlocal variables and widgets.
        """

        nonlocal results, captions, input_image_int, new_image, rank

        if input_image_int is None:
            messagebox.showinfo("Info", "Select your file!")
        else:
            results.append(input_image_int)
            captions.append(f"Rank-{rank} image")
            plot_images_tk(results, captions, root, new_image)

            new_image = True
            results, captions = [], []  # initialize nonlocal variables
            input_image_int = None
            rank = 1

        button_selection.config(text="Select File")
        scale_rank.config(from_=1, to=100, tickinterval=99)
        var.set(1)

    def check_call_svd():
        """
        This function checks to see if the setup is correct,
        calls the main function for compressing the given image by SVD,
        and plots the results.
        """

        nonlocal new_image
        # If this nonlocal variable is True, then SVD is newly performed
        # If this is False, then the SVD results obtained previously are reused

        if input_image_int is None:
            messagebox.showinfo("Info", "Select your file!")
        else:
            output_rank = var.get()     # Get the value from the scale widget below
            output_image_int = svd_image(
                input_image_int, output_rank, new_image
            )                           # Compress the image by SVD
            plot_images_tk(
                [output_image_int, input_image_int],
                [f"Rank-{output_rank} image", f"Original rank-{rank} image"],
                root, new_image
            )
            # Plot the resulting images
            new_image = False

            results.append(output_image_int)  # Stack the results for plot_all_reset
            captions.append(f"Rank-{output_rank}")

    ############################
    # GUI for the main program #
    ############################

    root = tk.Tk()
    root.title("Image compression by SVD")
    root.bind("<Return>", lambda event: check_call_svd())

    tk.Label(
        root, text="Select your image for compression",
        padx=15, pady=15
    ).pack(expand=tk.YES, fill=tk.BOTH)

    button_selection = tk.Button(
        root, text="Select File", command=select_image
    )
    button_selection.pack()

    tk.Label(
        root, text="Rank of the compressed image",
        padx=15, pady=15
    ).pack(expand=tk.YES, fill=tk.BOTH)

    var = tk.IntVar()
    scale_rank = tk.Scale(
        root, variable=var, showvalue=True, from_=1, to=100,
        length=290, tickinterval=99, orient=tk.HORIZONTAL, sliderlength=15)
    scale_rank.pack(padx=15)

    frame_buttons = tk.Frame(root)
    frame_buttons.pack(padx=15, pady=15)
    tk.Button(
        frame_buttons, text="Perform SVD",
        command=check_call_svd
    ).pack(side=tk.LEFT)
    tk.Button(
        frame_buttons, text="Plot all and reset",
        command=plot_all_reset
    ).pack(side=tk.RIGHT)

    root.mainloop()


if __name__ == "__main__":
    run_svd_image_scale()
