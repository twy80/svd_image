"""
Image Compression using SVD. by T.-W. Yoon, Aug. 2021
"""


def read_nonnegative_int(keyboard_message):
    """
    Print a message and read a non-negative integer from keyboard
    """
    no = input(keyboard_message)
    while True:
        try:
            number = int(no)
        except ValueError:
            pass
        else:
            if number >= 0:
                break
        no = input("One nonnegative integer please: ")

    return number


def read_image(keyboard_message):
    """
    Print a message and read an image file from keyboard
    """
    import imageio

    while True:
        image_file_name = input(keyboard_message)
        try:
            input_image = imageio.imread(image_file_name)
        except (OSError, SyntaxError, ValueError) as exception_caught:
            print(exception_caught, " Try again.", sep=".")
        else:
            break

    return input_image


def run_svd_image_cmd():
    """
    This program performs SVD of an image matrix, compresses it by reducing the rank,
    and uses the following functions:

    read_image:             reading an image file from the keyboard
    read_nonnegative_int:   reading the rank of the compressed image from the keyboard
    plot_images:            plotting images
    svd_image:              compressing the image by SVD, the main function.

    plot_images and svd_image are imported from svd_image_functions.py.
    """

    import numpy as np
    from svd_image_functions import svd_image, plot_images

    results, captions = [], []
    rank = 1

    # For investigating the results after running the code if necessary

    print("\nImage compression by SVD. Give an image file and values for the rank!")

    input_image_int = read_image("Enter the image file name: ")

    image_shape = input_image_int.shape

    channels = 1 if len(image_shape) == 2 else image_shape[2]
    # If the image is grayscale, channels = 1

    for i in range(channels):  # Compute the rank of each channel
        if channels == 1:
            rank = np.linalg.matrix_rank(input_image_int)
        else:
            rank = max(rank, np.linalg.matrix_rank(input_image_int[:, :, i]))

    print(f"\nRank of the original picture is {rank}.")
    
    new_image = True

    while True:  # Construct the images using SVD for various rank values
        output_rank = read_nonnegative_int("Type an Integer for Rank? (Type 0 to stop): ")
        if output_rank == 0:
            break  # Stop if n is zero
        elif output_rank > rank:
            output_rank = rank  # Constrain n to be between 1 and the rank

        output_image_int = svd_image(
            input_image_int, output_rank, new_image
        )                       # Compress the image by SVD

        plot_images(
            [output_image_int, input_image_int],
            [f"Rank-{output_rank} image", f"Original rank-{rank} image"],
            new_image
        )
        # Plot the resulting images

        new_image = False

        results.append(output_image_int)  # Stack the results for plot_all_reset
        captions.append(f"Rank-{output_rank}")

    results.append(input_image_int)
    captions.append(f"Rank-{rank} image")

    plot_images(results, captions)
    _ = input("\nPress enter to close the images.\n")


if __name__ == "__main__":
    run_svd_image_cmd()
