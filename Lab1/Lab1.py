import os
from PIL import Image, ImageEnhance
import tkinter as tk
from tkinter import filedialog
import pathlib


class Service:
    """
    Class for all file and user interaction operations (I/O, path handling, size calculations).
    It acts as a utility layer for the ImageProcessor.
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
        # Display all available formats from the ImageProcessor map keys.
        for key in ImageProcessor.ALL_IMAGE_FORMATS_MAP.keys():
            print(key, end=', ')
        print()
        while True:
            file_format = input("Your format: ")
            if file_format not in ImageProcessor.ALL_IMAGE_FORMATS_MAP.keys():
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
        Filters the files based on supported image formats defined in ImageProcessor.
        """
        self.file_paths = []
        # Initialize Tkinter for the dialog.
        root = tk.Tk()
        root.attributes('-topmost', True)
        root.withdraw()  # Hide the main Tkinter window

        # Define file types for the selection dialog.
        supported_extensions = list(ImageProcessor.ALL_IMAGE_FORMATS_MAP.values())
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


class ImageProcessor:
    """
    Class for all core image manipulation operations using the PIL (Pillow) library.
    """
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

    def __init__(self):
        self.image_paths = None
        self.output_path = None
        # Initialize the utility service class.
        self.service = Service()

    def convert_image_format(self):
        """
        Converts a batch of selected images to a user-specified format.
        Handles transparency/color-mode conversion for formats that don't support it (e.g., JPEG, BMP).
        """
        files = self.service.get_images()
        targeted_format = self.service.get_targeted_format()
        output_dir = self.service.get_output_dir()

        for i in files:
            img = Image.open(i)
            # Handle transparency (RGBA/P) for formats that don't support it well (JPEG, BMP).
            if targeted_format.upper() in ('JPEG', 'BMP') and img.mode in ('RGBA', 'P'):

                print(f"-> Find transparency ({img.mode}). Convert to RGB.")
                # Create a white background image.
                background = Image.new("RGB", img.size, (255, 255, 255))

                # Convert palette mode (P) to RGBA first if necessary.
                if img.mode == 'P':
                    img = img.convert('RGBA')

                # Paste the image onto the background using the alpha channel as a mask.
                # This effectively replaces transparency with white.
                background.paste(img, mask=img.split()[3])

                img = background.convert('RGB')
            # Convert CMYK mode to RGB, as many operations/formats prefer RGB.
            elif img.mode == 'CMYK':
                img = img.convert('RGB')

            # Construct the output file path.
            filename = pathlib.Path(i).stem
            extension = self.ALL_IMAGE_FORMATS_MAP[targeted_format]
            output_path = output_dir + "\\" + filename + extension

            # Save the image with the new format and a quality setting of 90 (for lossy formats).
            img.save(output_path, format=targeted_format, quality=90)
            img.close()
            # Compare and print the size change.
            self.service.compare_file_size(i, output_path)

    def convert_image_size(self, command):
        """
        Resizes all selected images based on the user's choice:
        'H' (height), 'W' (width), or 'HW' (both height and width).
        Uses Image.Resampling.LANCZOS for high-quality downsampling/resizing.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        # Determine the resizing method based on the command.
        match command:
            case 'H':
                for i in files:
                    img = Image.open(i)
                    current_size = img.size
                    # Calculate new size based on user-input height, maintaining ratio.
                    new_size = self.service.calculate_size_by_height(current_size)
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    # Save the resized image with a "_resized" suffix.
                    filename = pathlib.Path(i).stem + "_resized" + pathlib.Path(i).suffix
                    output_path = pathlib.Path(output_dir) / filename
                    resized_img.save(output_path)
            case 'W':
                for i in files:
                    img = Image.open(i)
                    current_size = img.size
                    # Calculate new size based on user-input width, maintaining ratio.
                    new_size = self.service.calculate_size_by_width(current_size)
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    # Save the resized image.
                    filename = pathlib.Path(i).stem + "_resized" + pathlib.Path(i).suffix
                    output_path = pathlib.Path(output_dir) / filename
                    resized_img.save(output_path)
            case 'HW':
                for i in files:
                    img = Image.open(i)
                    # Get new size from user-input width and height (ratio not necessarily maintained).
                    new_size = self.service.calculate_size_by_height_and_width()
                    resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                    # Save the resized image.
                    filename = pathlib.Path(i).stem + "_resized" + pathlib.Path(i).suffix
                    output_path = pathlib.Path(output_dir) / filename
                    resized_img.save(output_path)

    def convert_image_color(self):
        """
        Converts a specific old RGB color in the selected images to a new RGB color.
        Performs a pixel-by-pixel check and replacement.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        # Get old and new colors from the user in 'r g b' format.
        r, g, b = map(int, input("Input old color in r g b (for example 255 0 0 )):").split(" "))
        old_color = (r, g, b)
        r, g, b = map(int, input("Input new color in r g b (for example 255 0 0 )):").split(" "))
        new_color = (r, g, b)

        for i in files:
            img = Image.open(i)
            # Convert to RGB mode to ensure consistency for color manipulation.
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Load pixels for direct manipulation.
            pixels = img.load()
            width, height = img.size

            print(f"Розмір зображення: {width}x{height} пікселів.")

            changes_count = 0

            # Iterate through every pixel.
            for x in range(width):
                for y in range(height):
                    current_color = pixels[x, y]

                    # Compare the current pixel color with the target 'old_color'.
                    if current_color == old_color:
                        # Change the pixel color.
                        pixels[x, y] = new_color
                        changes_count += 1

            print(f"Color change completed. Changed {changes_count} pixels.")
            # Save the recolored image.
            filename = pathlib.Path(i).stem + "_recolored" + pathlib.Path(i).suffix
            output_path = pathlib.Path(output_dir) / filename
            img.save(output_path)

    def image_color_balance(self, mode):
        """
        Adjusts the color balance (R, G, B) or overall brightness (ALL) of selected images.
        Uses ImageEnhance.Brightness for 'ALL' mode and manual pixel manipulation for R/G/B.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        # Get the balance factor (e.g., 1.2 for 20% increase, 0.8 for 20% decrease).
        factor = float(input(
            "Input balance factor (for example: 1.2 will increase color/brightness by 20%, 0.8 will decrees by 20%): "))

        for i in files:
            img = Image.open(i)

            if mode == "ALL":
                # Use PIL's built-in Brightness enhancer for overall brightness.
                enhancer = ImageEnhance.Brightness(img)
                img_output = enhancer.enhance(factor)
                # Save the balanced image.
                filename = pathlib.Path(i).stem + "_balanced" + pathlib.Path(i).suffix
                output_path = pathlib.Path(output_dir) / filename
                img_output.save(output_path)
            else:
                # Manual channel balancing for R, G, or B.
                # Ensure image is in RGB mode for consistent indexing.
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                pixels = img.load()
                width, height = img.size
                # Map mode ('R', 'G', 'B') to the corresponding index (0, 1, 2).
                channel_index = {'R': 0, 'G': 1, 'B': 2}.get(mode)

                for x in range(width):
                    for y in range(height):
                        current_color = list(pixels[x, y])
                        # Calculate the new channel value.
                        new_value = int(current_color[channel_index] * factor)
                        # Clamp the new value between 0 and 255.
                        current_color[channel_index] = max(0, min(255, new_value))
                        # Update the pixel color.
                        pixels[x, y] = tuple(current_color)

                # Save the balanced image.
                filename = pathlib.Path(i).stem + "_balanced" + pathlib.Path(i).suffix
                output_path = pathlib.Path(output_dir) / filename
                img.save(output_path)


class Menu:
    """
    Handles the user interface and navigation for the terminal-based application.
    It orchestrates calls to the ImageProcessor based on user input.
    """

    def __init__(self):
        self.choice = None  # Stores the current user menu choice.
        self.processor = ImageProcessor()  # Initialize the image processing core.

    def main_menu(self):
        """
        Displays the main menu options and handles user selection.
        """
        print("\nWhat do you want to do?")
        print("1. Convert image format")
        print("2. Convert image size")
        print("3. Convert colors")
        print("4. Color correction")
        self.choice = input('Input your choice: ')

        # Directs flow based on user choice.
        match self.choice:
            case '1':
                self.processor.convert_image_format()
                # Prompt to continue or exit.
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '2':
                self.size_menu()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '3':
                self.processor.convert_image_color()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '4':
                self.color_balance_menu()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case _:
                print("Wrong command, try again.")
                self.main_menu()

    def size_menu(self):
        """
        Displays the image resizing sub-menu.
        """
        print(f"\nWhat do you want to do?")
        print("1. Convert size by height (maintains aspect ratio)")
        print("2. Convert size by width (maintains aspect ratio)")
        print("3. Convert size by height and width (may change aspect ratio)")
        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.processor.convert_image_size("H")
            case '2':
                self.processor.convert_image_size("W")
            case '3':
                self.processor.convert_image_size("HW")
            case _:
                print("Wrong command, try again.")
                self.size_menu()

    def color_balance_menu(self):
        """
        Displays the color balance sub-menu.
        """
        print(f"\nWhat do you want to do?")
        print("1. Balance red color")
        print("2. Balance green color")
        print("3. Balance blue color")
        print("4. Balance overall brightness")

        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.processor.image_color_balance("R")
            case '2':
                self.processor.image_color_balance("G")
            case '3':
                self.processor.image_color_balance("B")
            case '4':
                self.processor.image_color_balance("ALL")
            case _:
                print("Wrong command, try again.")
                self.color_balance_menu()


def main():
    """
    Entry point of the program.
    """
    menu = Menu()
    menu.main_menu()


if __name__ == "__main__":
    # Execute main() when the script is run directly.
    main()
