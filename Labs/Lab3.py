from PIL import Image, ImageDraw, ImageFont, ImageTk
from Common import Service, ALL_IMAGE_FORMATS_MAP
import pathlib
import os
import tkinter as tk


class Lab3Processor:
    def __init__(self):
        self.service = Service()

    def combine_images(self):
        """
        Task 1: Combine two images horizontally or vertically.
        """
        print("Please select exactly TWO images to combine.")
        files = self.service.get_images()

        if len(files) != 2:
            print(f"Error: You selected {len(files)} images. Please select exactly 2.")
            return

        direction = input("Combine horizontally (H) or vertically (V)? ").upper()
        if direction not in ('H', 'V'):
            print("Wrong direction. Please input 'H' or 'V'.")
            return

        output_dir = self.service.get_output_dir()

        try:
            # Open and convert to RGB to avoid transparency issues
            img1 = Image.open(files[0]).convert('RGB')
            img2 = Image.open(files[1]).convert('RGB')

            w1, h1 = img1.size
            w2, h2 = img2.size

            if direction == 'H':
                # Horizontal combination
                new_width = w1 + w2
                new_height = max(h1, h2)
                new_img = Image.new('RGB', (new_width, new_height))
                new_img.paste(img1, (0, 0))
                new_img.paste(img2, (w1, 0))

            else:  # direction == 'V'
                # Vertical combination
                new_width = max(w1, w2)
                new_height = h1 + h2
                new_img = Image.new('RGB', (new_width, new_height))
                new_img.paste(img1, (0, 0))
                new_img.paste(img2, (0, h1))

            # Create output filename
            stem1 = pathlib.Path(files[0]).stem
            stem2 = pathlib.Path(files[1]).stem
            filename = f"{stem1}_{stem2}_combined.png"  # Save as PNG
            output_path = pathlib.Path(output_dir) / filename

            new_img.save(output_path)
            print(f"Combined image saved as {filename}")

        except Exception as e:
            print(f"An error occurred during image combining: {e}")

    def add_watermark(self):
        """
        Task 2: Add a text watermark to an image.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()

        # Get parameters from the user
        try:
            text = input("Enter watermark text: ")
            pos_choice = input("Position (TL - top-left, C - center, BR - bottom-right): ").upper()
            font_size = int(input("Enter font size (e.g., 36): "))
            opacity = int(input("Enter opacity (0-255, 0=transparent, 255=opaque): "))
            color_str = input("Enter color (R,G,B), e.g., '255,255,255': ")

            r, g, b = map(int, color_str.split(','))
            text_color = (r, g, b, opacity)  # Color with opacity

        except ValueError:
            print("Invalid input. Please check your numbers.")
            return

        # Try to load the font
        try:
            # Arial is available on most systems.
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            print("Arial font not found, using default font.")
            font = ImageFont.load_default()

        for i in files:
            try:
                # Convert to RGBA to be able to overlay a layer with transparency
                img = Image.open(i).convert("RGBA")
                width, height = img.size

                # Create a separate transparent layer for the text
                txt_layer = Image.new("RGBA", img.size, (255, 255, 255, 0))
                draw = ImageDraw.Draw(txt_layer)

                # Determine the text size
                # Use textbbox to get precise text boundaries
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]

                # Determine the position
                padding = 10  # Padding from the edges
                if pos_choice == 'C':
                    x = (width - text_width) // 2
                    y = (height - text_height) // 2
                elif pos_choice == 'BR':
                    x = width - text_width - padding
                    y = height - text_height - padding
                elif pos_choice == 'TL':
                    x = padding
                    y = padding
                else:  # Default to center
                    print("Invalid position, defaulting to center.")
                    x = (width - text_width) // 2
                    y = (height - text_height) // 2

                # Draw text on the transparent layer
                draw.text((x, y), text, font=font, fill=text_color)

                # Composite the original image and the text layer
                watermarked_img = Image.alpha_composite(img, txt_layer)

                # Save (must be PNG to support transparency)
                filename = pathlib.Path(i).stem + "_watermarked.png"
                output_path = pathlib.Path(output_dir) / filename
                watermarked_img.save(output_path)
                print(f"Watermarked image saved as {filename}")

            except Exception as e:
                print(f"Failed to watermark {i}: {e}")

    def create_slideshow(self):
        """
        Task 3: Create a slideshow from selected images.
        """
        print("Please select the images for the slideshow.")
        # Use get_images() to select files
        image_files = self.service.get_images()

        if not image_files:
            print("No images selected.")
            return

        try:
            delay = int(input("Enter delay between slides (in seconds): "))
        except ValueError:
            print("Invalid delay. Defaulting to 2 seconds.")
            delay = 2

        delay_ms = delay * 1000  # Convert to milliseconds for .after()

        # The image_files list is already prepared,
        # so the block for searching files in a directory is no longer needed.

        print(f"Found {len(image_files)} images. Starting slideshow...")

        # Setup Tkinter GUI
        root = tk.Tk()
        root.title("Slideshow")
        label = tk.Label(root)
        label.pack()

        # Use .after() instead of time.sleep() to avoid blocking the GUI
        def update_image(index):
            img_path = image_files[index]
            try:
                img = Image.open(img_path)
                img.thumbnail((800, 600))

                # Use 'master=root' to avoid errors
                tk_img = ImageTk.PhotoImage(img, master=root)
                label.config(image=tk_img)
                label.image = tk_img
            except Exception as e:
                print(f"Could not load image {img_path}: {e}")

            next_index = index + 1

            # Check if there are more images in the list
            if next_index < len(image_files):
                # If yes, schedule the next image
                root.after(delay_ms, update_image, next_index)
            else:
                # If no (this was the last image),
                # wait for the same delay and close the window
                print("Slideshow finished.")

                def close_slideshow():
                    root.destroy()  # 1. Destroy the window
                    root.quit()  # 2. Explicitly stop the mainloop

                root.after(delay_ms, close_slideshow)  # Call our new function

        try:
            update_image(0)
            root.mainloop()
        except tk.TclError:
            print("Slideshow window closed.")
