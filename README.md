# Image Processor for "Computer Graphics and Visualization"

This project was created as a series of laboratory works for the university course "Computer Graphics and Visualization". It is a console-based image processing application written in Python that allows users to perform a variety of image manipulation tasks through a simple, interactive menu.

## Description

The application provides a command-line interface to apply various effects and modifications to images. It's organized in "labs" each with a different set of functionalities. The user can select one or more images, and then choose from a menu of operations to apply to them. The processed images are saved to a user-specified output directory.

## Features

### Lab 1: Core Image Manipulations
* **Format Conversion:** Convert images between various formats like PNG, JPEG, BMP, GIF, and TIFF.
* **Resizing:** Resize images by height, width, or both (aspect ratio handled).
* **Color Replacement:** Replace a specific RGB color in an image with another.
* **Color Balance:** Adjust R, G, B channels or overall brightness.

### Lab 2: Advanced Image Manipulations
* **Transparency:** Modify the alpha channel of an image.
* **Cropping:** Standard crop, inverse crop (transparent hole), and slicing images.
* **Contrast Enhancement:** Increase or decrease image contrast.

### Lab 3: Composition & Presentation
* **Combine Images:** Join two images horizontally or vertically.
* **Watermarking:** Add text watermarks with customizable font, opacity, position, and color.
* **Slideshow:** View selected images in a simple slideshow with adjustable delay.

### Lab 4: Analysis & Simple Conversion
* **Analysis:**
    * Display images using the default viewer.
    * Output the brightness matrix (NumPy array) to the console.
    * Generate and display color and grayscale histograms (using Matplotlib).
* **Conversions:**
    * **Binarization:** Convert images to black and white based on a threshold.
    * **Grayscale:** Convert color images to shades of gray.
    * **Negative:** Invert the colors of an image.

### Lab 5: Filtering & Edge Detection
* **Edge Detection:** Implementation of the **Roberts Cross Operator** (Variant 5) to highlight edges in images.

## Requirements

* Python 3
* Pillow (the Python Imaging Library fork)
* Tkinter (usually included with Python)
* NumPy (for matrix operations in Lab 4 & 5)
* Matplotlib (for histograms in Lab 4)

You can install the required libraries using pip:

```bash
pip install Pillow numpy matplotlib
```
## How to run
1. Navigate to the [Labs](https://github.com/AvensTach/graphics/tree/main/Labs) directory.
2. Run the [Main.py](https://github.com/AvensTach/graphics/blob/main/Labs/Main.py) script from your terminal:
```bash
python Main.py
```
3. Follow the on-screen prompts to select images and choose the desired operations.

## License
This project is licensed under the MIT License. See the [LICENSE](https://github.com/AvensTach/graphics/blob/main/LICENSE) file for details.