from PIL import Image, ImageFilter
import numpy as np
import pathlib
from Common import Service


class Lab6Processor:
    """
    Class for noise reduction and filter analysis (Lab 6).
    Uses ONLY built-in PIL framework functions.
    """

    def __init__(self):
        self.service = Service()
        self.test_dir = "Tests_for_lab_6"  # Папка з файлами 0.bmp ... 8.bmp

    def calculate_mse(self, original_img, filtered_img):
        """
        Calculates Mean Squared Error (MSE) using NumPy for analysis.
        Note: This is an analysis metric, not a filter implementation.
        """
        arr_orig = np.asarray(original_img, dtype="float")
        arr_filt = np.asarray(filtered_img, dtype="float")

        diff = arr_orig - arr_filt
        sq_diff = diff ** 2
        mse = np.mean(sq_diff)
        return mse

    def run_analysis(self):
        """
        Main execution method for Lab 6.
        """
        print(f"Looking for test images in folder: ./{self.test_dir}/")

        # --- 1. Define Filter Set using ONLY PIL.ImageFilter ---
        # Використовуємо вбудовані класи фільтрів.
        # Для отримання 7 нелінійних фільтрів варіюємо типи та розміри ядра.

        filters = [
            # === Linear Filters (3 required) ===
            ("Box Blur (3x3)", ImageFilter.BoxBlur(1), "Linear"),  # Radius 1 -> 3x3 kernel
            ("Gaussian Blur (R=2)", ImageFilter.GaussianBlur(2), "Linear"),
            ("Unsharp Mask", ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3), "Linear"),

            # === Non-Linear Filters (7 required) ===
            # 1. Median 3x3 (Standard noise removal)
            ("Median (3x3)", ImageFilter.MedianFilter(size=3), "Non-Linear"),

            # 2. Median 5x5 (Stronger noise removal)
            ("Median (5x5)", ImageFilter.MedianFilter(size=5), "Non-Linear"),

            # 3. Min Filter 3x3 (Erodes bright noise)
            ("Min Filter (3x3)", ImageFilter.MinFilter(size=3), "Non-Linear"),

            # 4. Max Filter 3x3 (Dilates dark noise)
            ("Max Filter (3x3)", ImageFilter.MaxFilter(size=3), "Non-Linear"),

            # 5. Min Filter 5x5 (Stronger erosion)
            ("Min Filter (5x5)", ImageFilter.MinFilter(size=5), "Non-Linear"),

            # 6. Max Filter 5x5 (Stronger dilation)
            ("Max Filter (5x5)", ImageFilter.MaxFilter(size=5), "Non-Linear"),

            # 7. Mode Filter 3x3 (Frequent pixel value, good for speckled noise)
            ("Mode Filter (3x3)", ImageFilter.ModeFilter(size=3), "Non-Linear"),
        ]

        # --- 2. Load Reference Image ---
        ref_path = pathlib.Path(self.test_dir) / "0.bmp"
        if not ref_path.exists():
            print(f"Error: Reference image '0.bmp' not found in {self.test_dir}.")
            return

        try:
            ref_img = Image.open(ref_path).convert('L')
        except Exception as e:
            print(f"Error loading reference image: {e}")
            return

        # --- 3. Process All Images ---
        print(f"{'Image':<10} | {'Filter Name':<25} | {'Type':<10} | {'MSE':<10}")
        print("-" * 65)

        # Обробляємо зображення від 0.bmp до 8.bmp
        for i in range(9):
            file_name = f"{i}.bmp"
            file_path = pathlib.Path(self.test_dir) / file_name

            if not file_path.exists():
                continue

            try:
                # Відкриваємо та конвертуємо в градації сірого (L)
                current_img = Image.open(file_path).convert('L')

                for f_name, f_obj, f_type in filters:
                    # Застосування вбудованого фільтра PIL
                    filtered_img = current_img.filter(f_obj)

                    # Розрахунок помилки відносно еталону (0.bmp)
                    mse = self.calculate_mse(ref_img, filtered_img)

                    print(f"{file_name:<10} | {f_name:<25} | {f_type:<10} | {mse:.2f}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

        print("-" * 65)
        print("Analysis completed.")