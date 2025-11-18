from PIL import Image
import numpy as np
from Common import Service
import pathlib


class Lab5Processor:
    """
    Class for image filtering and edge detection operations (Lab 5).
    """

    def __init__(self):
        self.service = Service()

    def roberts_edge_detection(self):
        """
        Task: Edge detection using Roberts Cross Operator.
        This algorithm highlights regions of high spatial gradient (edges).
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        if not files or not output_dir:
            print("Files or output directory not selected.")
            return

        for i in files:
            try:
                img = Image.open(i)
                # Convert to grayscale ('L')
                gray_img = img.convert('L')

                # Use int32 for calculations to avoid overflow/underflow during subtraction
                img_array = np.asarray(gray_img, dtype="int32")

                # Roberts Cross Calculation
                # Gx = P(x,y) - P(x+1, y+1)
                gx = img_array[:-1, :-1] - img_array[1:, 1:]

                # Gy = P(x, y+1) - P(x+1, y)
                gy = img_array[:-1, 1:] - img_array[1:, :-1]

                # Calculate Gradient Magnitude
                gradient = np.sqrt(gx ** 2 + gy ** 2)

                # Roberts operator often produces weak values.
                # Normalizing (stretching) the result to 0-255 makes edges more visible.
                max_val = gradient.max()
                if max_val > 0:
                    gradient = (gradient / max_val) * 255

                # Convert gradient to uint8
                gradient = gradient.astype('uint8')

                # We explicitly use dtype=np.uint8.
                # If we used zeros_like(img_array), it would be int32, causing the "Black Image" bug.
                h, w = img_array.shape
                roberts_img = np.zeros((h, w), dtype=np.uint8)

                # Place the result (which is 1 pixel smaller) into the image
                roberts_img[:-1, :-1] = gradient

                # Create image from uint8 array -> Creates Mode 'L' (Standard Grayscale)
                final_img = Image.fromarray(roberts_img)

                filename = pathlib.Path(i).stem + "_roberts" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                final_img.save(output_path)
                print(f"Edge detection completed. Saved as: {filename}")

            except Exception as e:
                print(f"Failed to process {i}: {e}")