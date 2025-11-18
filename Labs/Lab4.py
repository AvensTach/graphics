from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from Common import Service
import pathlib


class Lab4Processor:
    """
    Class for image analysis operations and simple transformations
    (Lab 4).
    """

    def __init__(self):
        self.service = Service()

    def show_images(self):
        """
        Task 1: Display the original color image on the screen.
        """
        files = self.service.get_images()
        if not files:
            print("Files not selected.")
            return

        print(f"Showing {len(files)} images...")
        for i in files:
            try:
                img = Image.open(i)
                # .show() opens the image in the standard viewer
                img.show(title=pathlib.Path(i).name)
            except Exception as e:
                print(f"Failed to open {i}: {e}")

    def show_brightness_matrix(self):
        """
        Task 2: Display the brightness value matrix on the screen.
        """
        files = self.service.get_images()
        if not files:
            print("Files not selected.")
            return

        for i in files:
            try:
                img = Image.open(i)
                # Convert to grayscale ('L' - luminance)
                grayscale_img = img.convert('L')

                # Convert image to NumPy matrix
                brightness_matrix = np.array(grayscale_img)

                print(f"\n--- Brightness Matrix for {pathlib.Path(i).name} ---")
                # np.set_printoptions(threshold=np.inf) # Uncomments to disable output limit
                print(brightness_matrix)

            except Exception as e:
                print(f"Failed to process {i}: {e}")

    def show_color_histogram(self):
        """
        Task 3: Construct a brightness histogram for a color image.
        """
        files = self.service.get_images()
        if not files:
            print("Files not selected.")
            return

        for i in files:
            try:
                img = Image.open(i)
                # Ensure image is RGB to split channels
                rgb_img = img.convert('RGB')

                # .histogram() returns a list of 256 values for each channel
                # We split channels to get 3 separate histograms
                r_hist = rgb_img.getchannel('R').histogram()
                g_hist = rgb_img.getchannel('G').histogram()
                b_hist = rgb_img.getchannel('B').histogram()

                plt.figure(figsize=(10, 6))
                plt.title(f'Color Histogram for {pathlib.Path(i).name}')
                plt.plot(r_hist, color='red', alpha=0.7, label='Red')
                plt.plot(g_hist, color='green', alpha=0.7, label='Green')
                plt.plot(b_hist, color='blue', alpha=0.7, label='Blue')
                plt.xlabel('Pixel Value')
                plt.ylabel('Frequency')
                plt.legend()
                plt.grid(True)
                plt.show()  # Opens Matplotlib window with the graph

            except Exception as e:
                print(f"Failed to plot histogram for {i}: {e}")

    def show_grayscale_histogram(self):
        """
        Task 4 (partial): Construct a grayscale histogram.
        """
        files = self.service.get_images()
        if not files:
            print("Files not selected.")
            return

        for i in files:
            try:
                img = Image.open(i)
                grayscale_img = img.convert('L')

                # .histogram() for 'L' mode returns a single histogram
                grayscale_hist = grayscale_img.histogram()

                plt.figure(figsize=(10, 6))
                plt.title(f'Grayscale Histogram for {pathlib.Path(i).name}')
                plt.plot(grayscale_hist, color='black')
                plt.xlabel('Brightness Value (0-255)')
                plt.ylabel('Frequency')
                plt.fill_between(range(256), grayscale_hist, color='gray', alpha=0.5)
                plt.grid(True)
                plt.show()

            except Exception as e:
                print(f"Failed to plot histogram for {i}: {e}")

    def convert_to_grayscale(self):
        """
        Task 4: Convert to shades of gray.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()
        if not files or not output_dir:
            return

        for i in files:
            try:
                img = Image.open(i)
                grayscale_img = img.convert('L')

                filename = pathlib.Path(i).stem + "_grayscale" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                grayscale_img.save(output_path)
                print(f"Saved in grayscale: {filename}")

            except Exception as e:
                print(f"Failed to convert {i}: {e}")

    def invert_image(self):
        """
        Task 4: Negative.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()
        if not files or not output_dir:
            return

        for i in files:
            try:
                img = Image.open(i)
                # Invert works correctly with RGB
                rgb_img = img.convert('RGB')

                inverted_img = ImageOps.invert(rgb_img)

                filename = pathlib.Path(i).stem + "_inverted" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                inverted_img.save(output_path)
                print(f"Saved negative: {filename}")

            except Exception as e:
                print(f"Failed to invert {i}: {e}")

    def binarize_image(self):
        """
        Task 4: Binarization (Black and White).
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()
        if not files or not output_dir:
            return

        try:
            # Ask user for threshold
            threshold = int(input("Enter binarization threshold (0-255, default 128): ") or 128)
            if not 0 <= threshold <= 255:
                raise ValueError
        except ValueError:
            print("Invalid value. Using threshold 128.")
            threshold = 128

        for i in files:
            try:
                img = Image.open(i)
                grayscale_img = img.convert('L')

                # Use .point() to apply threshold
                # '1' - 1-bit image mode (black or white)
                binarized_img = grayscale_img.point(lambda p: 255 if p > threshold else 0, '1')

                filename = pathlib.Path(i).stem + "_binarized" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                binarized_img.save(output_path)
                print(f"Saved binarized image: {filename}")

            except Exception as e:
                print(f"Failed to binarize {i}: {e}")