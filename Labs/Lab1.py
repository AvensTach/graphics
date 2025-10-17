from PIL import Image, ImageEnhance
import pathlib

import Lab2
from Common import Service, ALL_IMAGE_FORMATS_MAP


class Lab1Processor:
    """
    Class for all core image manipulation operations using the PIL (Pillow) library.
    """

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
            extension = ALL_IMAGE_FORMATS_MAP[targeted_format]
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
