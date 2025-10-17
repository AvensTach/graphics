import tkinter as tk
from tkinter import filedialog
import os

# Map of user-friendly format names to their standard file extensions.
ALL_IMAGE_FORMATS_MAP = {
    'png': '.png',
    'jpg': '.jpg',
    'jpeg': '.jpeg',
    'bmp': '.bmp',
    'gif': '.gif',
    'tiff': '.tiff',
    'psd': '.psd',
}


class Service:
    """
    Class for all file and user interaction operations (I/O, path handling, size calculations).
    It acts as a utility layer for the Lab1Processor.
    """

    def __init__(self):
        # Stores the paths of the files selected by the user.
        self.file_paths = None

    def get_targeted_format(self):
        """
        Prompts the user to select an image format for conversion from the console.
        Ensures the input format is valid and converts 'jpg' to 'jpeg' for PIL compatibility.
        """
        print("available formats:")
        # Display all available formats from the Lab1Processor map keys.
        for key in ALL_IMAGE_FORMATS_MAP.keys():
            print(key, end=', ')
        print()
        while True:
            file_format = input("Your format: ")
            if file_format not in ALL_IMAGE_FORMATS_MAP.keys():
                print("Wrong format, please try again.")
            else:
                break
        # PIL prefers 'jpeg' over 'jpg' for saving.
        if file_format == 'jpg':
            file_format = 'jpeg'

        return file_format

    def get_output_dir(self):
        """
        Opens a graphical dialog window for the user to choose the output directory.
        Uses Tkinter's filedialog.
        """
        # Initialize Tkinter root window.
        root = tk.Tk()
        # Ensure the dialog window appears above other applications.
        root.attributes('-topmost', True)
        # Hide the main Tkinter window.
        root.withdraw()

        print("Choose output dir:")

        # Use askdirectory to select a folder instead of files.
        output_directory = filedialog.askdirectory(
            title="Choose output dir"
        )

        # Destroy the Tkinter root object after use.
        root.destroy()

        return output_directory

    def get_images(self):
        """
        Opens a graphical dialog window for the user to select one or more image files.
        Filters the files based on supported image formats defined in Lab1Processor.
        """
        self.file_paths = []
        # Initialize Tkinter for the dialog.
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.withdraw()  # Hide the main Tkinter window

        # Define file types for the selection dialog.
        supported_extensions = list(ALL_IMAGE_FORMATS_MAP.values())
        file_types = [
            ("Supported Image Files", " ".join(
                f"*{ext}" for ext in supported_extensions
            )),
            ("All Files", "*.*")
        ]
        print("Please select your images")
        # Open the file selection dialog.
        self.file_paths = filedialog.askopenfilenames(
            title="Select Image Files",
            filetypes=file_types
        )
        return self.file_paths

    def compare_file_size(self, file_before, file_after):
        """
        Calculates and prints the file size before and after conversion/processing in MB.
        1048576 bytes = 1 MB.
        """
        # Get size in bytes and convert to MB.
        size_1 = os.path.getsize(file_before) / 1048576
        size_2 = os.path.getsize(file_after) / 1048576
        print("-----------------------------------")
        print(f"Size before convertion: {size_1:.2f}Mb")
        print(f"Size after convertion: {size_2:.2f}Mb")
        print(f"Change in size: {size_2 - size_1:.2f}Mb")
        print("-----------------------------------")

    def calculate_size_by_height_and_width(self):
        """
        Prompts the user for both new width and height for image resizing.
        """
        size = (int(input("Input your width")), int(input("Input your height")))
        return size

    def calculate_size_by_height(self, old_size):
        """
        Prompts the user for a new height and calculates the corresponding width
        to maintain the original aspect ratio.
        """
        new_height = int(input("Input new height: "))
        # Calculate the aspect ratio (width / height).
        ratio: float | int = old_size[0] / old_size[1]
        # Calculate the new width based on the ratio.
        new_width: int = int(new_height * ratio)
        new_size = (new_width, new_height)
        return new_size

    def calculate_size_by_width(self, old_size):
        """
        Prompts the user for a new width and calculates the corresponding height
        to maintain the original aspect ratio.
        """
        new_width = int(input("Input new width: "))
        # Calculate the inverse aspect ratio (height / width).
        ratio: float | int = old_size[1] / old_size[0]
        # Calculate the new height based on the ratio.
        new_height: int = int(new_width * ratio)
        new_size = (new_width, new_height)
        return new_size
