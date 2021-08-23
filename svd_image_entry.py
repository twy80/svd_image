"""
Image Compression using SVD. by T.-W. Yoon, Aug. 2021
"""


def run_svd_image_entry():
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
    from svd_image_functions import svd_image, plot_images_tk

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

        import numpy as np
        import imageio
        import tkinter.filedialog as fd
        # tk.Tk().withdraw()
        nonlocal input_image_int, rank

        image_file_name = fd.askopenfilename(
            title='Select a file!',
            filetypes=[('image files', '.bmp .jpg .jpeg .png .gif'), ('all files', '*')]
        )

        try:
            input_image_int = imageio.imread(image_file_name)
        except (SyntaxError, ValueError):
            messagebox.showinfo("Info", "Give a valid image file!")
        else:
            image_shape = input_image_int.shape

            channels = 1 if len(image_shape) == 2 else image_shape[2]
            # If the image is grayscale, channels = 1

            for i in range(channels):  # Compute the rank of each channel
                if channels == 1:
                    rank = np.linalg.matrix_rank(input_image_int)
                else:
                    rank = max(rank, np.linalg.matrix_rank(input_image_int[:, :, i]))

            button_selection.config(text=f"{image_shape[0]}x{image_shape[1]} image (rank = {rank})")

    def plot_all_reset():
        """
        This function plots all the results, and initializes the nonlocal variables and widgets.
        """

        nonlocal results, captions, input_image_int, new_image, rank

        if input_image_int is None:
            messagebox.showinfo("Info", "Select your file!")
        else:
            new_image = True
            results.append(input_image_int)
            captions.append(f"Rank-{rank} image")
            plot_images_tk(results, captions, root, new_image)

            results, captions = [], []  # initialize nonlocal variables
            input_image_int = None
            rank = 1

        button_selection.config(text="Select File")

    def check_call_svd():
        """
        This function checks to see if the setup is correct,
        calls the main function for compressing the given image by SVD,
        and plots the results.
        """

        nonlocal new_image
        # If this nonlocal variable is True, then SVD is newly performed
        # If this is False, then the SVD results obtained previously are reused

        msg_valid_number = f"Enter an integer between 1 and {rank}"

        if input_image_int is None:
            messagebox.showinfo("Info", "Select your file!")
        else:
            try:
                output_rank = int(entry_value.get())
            except ValueError:
                messagebox.showinfo("Info", msg_valid_number)
            else:
                if 1 <= output_rank <= rank:
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
                else:
                    messagebox.showinfo("Info", msg_valid_number)

    ############################
    # GUI for the main program #
    ############################

    base_color = {"bg": "white", "fg": "black"}
    root = tk.Tk()
    root.title("Image compression by SVD")
    root.config(bg="white")
    root.bind("<Return>", lambda event: check_call_svd())

    tk.Label(
        root, text="Select your image for compression",
        **base_color, padx=15, pady=15
    ).pack(expand=tk.YES, fill=tk.BOTH)

    button_selection = tk.Button(
        root, **base_color, text="Select File",
        command=select_image
    )
    button_selection.pack()

    frame_number = tk.Frame(root, bg="white")
    frame_number.pack(padx=15, pady=15)
    tk.Label(
        frame_number, **base_color,
        text="Rank of the output image  \u21D2 "
    ).pack(side=tk.LEFT)
    entry_value = tk.Entry(frame_number, **base_color, bd=4, width=4)
    # entry_value.bind("<Return>", (lambda event: check_call_svd()))
    entry_value.pack(side=tk.RIGHT)

    frame_buttons = tk.Frame(root, bg="white")
    frame_buttons.pack(padx=15, pady=15)
    tk.Button(
        frame_buttons, **base_color,
        text="Perform SVD", command=check_call_svd
    ).pack(side=tk.LEFT)
    tk.Button(
        frame_buttons, **base_color,
        text="Plot all and reset", command=plot_all_reset
    ).pack(side=tk.RIGHT)

    root.mainloop()


if __name__ == "__main__":
    run_svd_image_entry()