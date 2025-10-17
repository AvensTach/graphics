from PIL import Image, ImageEnhance
from Common import Service
import pathlib


class Lab2Processor:
    def __init__(self):
        self.service = Service()

    def add_transparency(self):
        """
        Add or change alpha chanel in image.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        try:
            alpha_factor = float(input("Input alpha 0.0(fully transparent) to 1.0 (not transparent): "))
            if not 0.0 <= alpha_factor <= 1.0:
                raise ValueError
        except ValueError:
            print("Wrong value! Input number from 0.0(fully transparent) to 1.0 (not transparent).")
            return

        for i in files:
            img = Image.open(i)

            # Convert to RGBA
            img = img.convert("RGBA")

            # Get pixels
            pixels = img.getdata()

            new_pixels = []
            for item in pixels:  # item = (R, G, B, A)
                # Change only ALPHA chanel!!!
                new_pixels.append((item[0], item[1], item[2], int(item[3] * alpha_factor)))

            img.putdata(new_pixels)

            filename = pathlib.Path(i).stem + "_transparent" + ".png"  # Save in PNG for transparency
            output_path = pathlib.Path(output_dir) / filename
            img.save(output_path)
            print(f"Image {filename} saved with transparency.")

    def crop_image(self):
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        for i in files:
            img = Image.open(i)
            width, height = img.size
            print(f"Image size: {width}x{height}.")

            left = int(input("Input left border (x1): "))
            upper = int(input("Input upper border (y1): "))
            right = int(input("Input right border (must be bigger then left) (x2): "))
            lower = int(input("Input lower border (must be bigger then upper) (y2): "))

            cropped_img = img.crop((left, upper, right, lower))

            filename = pathlib.Path(i).stem + "_cropped" + pathlib.Path(i).suffix
            output_path = pathlib.Path(output_dir) / filename
            cropped_img.save(output_path)
            print(f"Cropped image save as {filename}.")

    def invert_crop(self):
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        for i in files:
            img = Image.open(i).convert("RGBA")
            width, height = img.size
            print(f"Image size: {width}x{height}.")

            left = int(input("Input left border (x1): "))
            upper = int(input("Input upper border (y1): "))
            right = int(input("Input right border (must be bigger then left) (x2): "))
            lower = int(input("Input lower border (must be bigger then upper) (y2): "))

            transparent_rect = Image.new('RGBA', (right - left, lower - upper), (0, 0, 0, 0))
            img.paste(transparent_rect, (left, upper))

            filename = pathlib.Path(i).stem + "_inverted_crop" + ".png"
            output_path = pathlib.Path(output_dir) / filename
            img.save(output_path)
            print(f"Saved with cropped area as {filename}.")

    def slice_image(self):
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        parts = int(input("How many parts to divide horizontally into?? "))

        for i in files:
            img = Image.open(i)
            width, height = img.size
            part_width = width // parts

            for j in range(parts):
                left = j * part_width
                upper = 0
                right = (j + 1) * part_width
                lower = height

                box = (left, upper, right, lower)
                part = img.crop(box)

                filename = f"{pathlib.Path(i).stem}_part_{j + 1}{pathlib.Path(i).suffix}"
                output_path = pathlib.Path(output_dir) / filename
                part.save(output_path)
                print(f"Part {j + 1} saved as {filename}.")

    def enhance_contrast(self):
        """
        Increase contrast.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        try:
            factor = float(input("Input contrast coefficient (For example, 1.5 for 50% increase): "))
        except ValueError:
            print("Wrong value!")
            return

        for i in files:
            img = Image.open(i)

            # Object which works with contrast
            enhancer = ImageEnhance.Contrast(img)

            # Applies changes
            img_enhanced = enhancer.enhance(factor)

            filename = pathlib.Path(i).stem + "_contrasted" + pathlib.Path(i).suffix
            output_path = pathlib.Path(output_dir) / filename
            img_enhanced.save(output_path)
            print(f"Changed image saved as {filename}.")
