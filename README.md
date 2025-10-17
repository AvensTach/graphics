# Image Processor for "Computer Graphics and Visualization"

This project was created as a series of laboratory works for the university course "Computer Graphics and Visualization)". It is a console-based image processing application written in Python that allows users to perform a variety of image manipulation tasks through a simple, interactive menu.

## Description

The application provides a command-line interface to apply various effects and modifications to images. It's organized in "labs" each with a different set of functionalities. The user can select one or more images, and then choose from a menu of operations to apply to them. The processed images are saved to a user-specified output directory.

## Features

### Lab 1: Core Image Manipulations

* **Format Conversion:** Convert images between various formats like PNG, JPEG, BMP, GIF, and TIFF.
* **Resizing:**
    * Resize images by specifying a new height (maintaining aspect ratio).
    * Resize images by specifying a new width (maintaining aspect ratio).
    * Resize images by specifying both a new width and height.
* **Color Replacement:** Replace a specific RGB color in an image with another color.
* **Color Balance:** Adjust the red, green, or blue channels of an image, or adjust the overall brightness.

### Lab 2: Advanced Image Manipulations

* **Transparency:** Add or modify the alpha channel of an image to make it more or less transparent.
* **Cropping:**
    * Crop images by specifying the coordinates of the desired area.
    * Perform an inverse crop, making the selected area transparent.
    * Slice an image into multiple vertical parts.
* **Contrast Enhancement:** Increase or decrease the contrast of an image.

## Requirements

* Python 3
* Pillow (the Python Imaging Library fork)
* Tkinter (for file dialogs)

You can install the required libraries using pip:

```bash
pip install Pillow
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