import numpy as np
from PIL import Image
import pathlib
import os

# --- CONFIGURATION CONSTANTS ---
ORIGINAL_IMAGE_PATH = r"C:\Users\Avens\Documents\KNU\VSprojects\PycharmProjects\graphics\Labs\Tests_for_lab_6\0.bmp"  # Name of your reference file
OUTPUT_DIR = "Tests_for_lab_6"  # New folder for saving results
IMAGE_SIZE = 128  # Expected size 128x128


def add_gaussian_noise(image_array, mean=0.0, variance=100.0):
    """
    Adds additive Gaussian noise.
    """
    sigma = variance ** 0.5
    noise = np.random.normal(mean, sigma, image_array.shape)
    noisy_array = image_array + noise

    # Clip values between 0 and 255
    noisy_array = np.clip(noisy_array, 0, 255)
    return noisy_array.astype(np.uint8)


def add_salt_and_pepper_noise(image_array, density=0.05):
    """
    Adds salt-and-pepper impulse noise.
    """
    noisy_array = image_array.copy()
    num_pixels = image_array.size
    num_noise = int(num_pixels * density)

    # Random coordinates for "Salt" (white pixels)
    rand_coords_salt = np.random.choice(num_pixels, num_noise // 2, replace=False)

    # Random coordinates for "Pepper" (black pixels)
    rand_coords_pepper = np.random.choice(num_pixels, num_noise // 2, replace=False)

    # Convert linear indices to 2D coordinates
    H, W = image_array.shape
    row_salt, col_salt = np.unravel_index(rand_coords_salt, (H, W))
    row_pepper, col_pepper = np.unravel_index(rand_coords_pepper, (H, W))

    noisy_array[row_salt, col_salt] = 255  # Salt
    noisy_array[row_pepper, col_pepper] = 0  # Pepper

    # FIX: Convert back to uint8 (0-255) so PIL can save it as BMP
    return noisy_array.astype(np.uint8)


def add_brightness_dependent_noise(image_array, base_variance=5.0, gain=0.1):
    """
    Spatially non-stationary noise where variance depends on brightness (Brighter = More noise).
    (Approximation of Poisson/Photon noise).
    """
    # Normalize so intensity (brightness) is between 0 and 1
    normalized_img = image_array / 255.0

    # Variance = Base_Variance + Gain * Brightness
    local_variance = base_variance + gain * normalized_img * 255.0

    noise = np.random.normal(0, np.sqrt(local_variance), image_array.shape)

    noisy_array = image_array + noise
    noisy_array = np.clip(noisy_array, 0, 255)
    return noisy_array.astype(np.uint8)


def add_coordinate_dependent_noise(image_array, max_variance=200.0):
    """
    Spatially non-stationary noise where variance is a function of spatial coordinates.
    Variance increases horizontally (from left to right).
    """
    H, W = image_array.shape

    # Create a variance mask that increases linearly from 0 to max_variance
    variance_mask = np.linspace(0, max_variance, W)
    # Stretch the mask across the full height of the image
    variance_map = np.tile(variance_mask, (H, 1))

    # Generate Gaussian noise with local variance
    noise = np.random.normal(0, np.sqrt(variance_map), image_array.shape)

    noisy_array = image_array + noise
    noisy_array = np.clip(noisy_array, 0, 255)
    return noisy_array.astype(np.uint8)


def generate_images():
    """
    Main function to generate test images.
    """
    try:
        # 1. Load reference image (0.bmp)
        img = Image.open(ORIGINAL_IMAGE_PATH).convert('L')  # 'L' for grayscale
    except FileNotFoundError:
        print(f"Error: Reference file not found: {ORIGINAL_IMAGE_PATH}")
        print("Ensure the file is located next to the script.")
        return
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    if img.size != (IMAGE_SIZE, IMAGE_SIZE):
        print(f"Error: Image size must be {IMAGE_SIZE}x{IMAGE_SIZE}, found {img.size}")
        return

    # Create output directory
    pathlib.Path(OUTPUT_DIR).mkdir(exist_ok=True)

    # Save reference image (Image 0)
    img.save(pathlib.Path(OUTPUT_DIR) / "0.bmp", 'bmp')
    print(f"Saved 0.bmp (Reference)")

    # Convert PIL Image to NumPy array for processing
    original_array = np.asarray(img, dtype="float")

    # --- 2. Generate Noisy Images (1-8) ---

    # Image 1: Additive noise, LOW variance (Variance = 100)
    array_1 = add_gaussian_noise(original_array, variance=100.0)
    Image.fromarray(array_1).save(pathlib.Path(OUTPUT_DIR) / "1.bmp", 'bmp')
    print("Saved 1.bmp (Additive noise, variance 100)")

    # Image 2: Additive noise, HIGH variance (Variance = 400)
    array_2 = add_gaussian_noise(original_array, variance=400.0)
    Image.fromarray(array_2).save(pathlib.Path(OUTPUT_DIR) / "2.bmp", 'bmp')
    print("Saved 2.bmp (Additive noise, variance 400)")

    # Image 3: Impulse noise, LOW density (Density = 2%)
    array_3 = add_salt_and_pepper_noise(original_array, density=0.02)
    Image.fromarray(array_3).save(pathlib.Path(OUTPUT_DIR) / "3.bmp", 'bmp')
    print("Saved 3.bmp (Impulse noise, 2% density)")

    # Image 4: Impulse noise, HIGH density (Density = 10%)
    array_4 = add_salt_and_pepper_noise(original_array, density=0.10)
    Image.fromarray(array_4).save(pathlib.Path(OUTPUT_DIR) / "4.bmp", 'bmp')
    print("Saved 4.bmp (Impulse noise, 10% density)")

    # Image 5: Spatially non-stationary noise, variance depends on BRIGHTNESS (Weak effect)
    array_5 = add_brightness_dependent_noise(original_array, gain=0.1)
    Image.fromarray(array_5).save(pathlib.Path(OUTPUT_DIR) / "5.bmp", 'bmp')
    print("Saved 5.bmp (Brightness-dependent noise, weak)")

    # Image 6: Spatially non-stationary noise, variance depends on BRIGHTNESS (Strong effect)
    array_6 = add_brightness_dependent_noise(original_array, gain=0.3)
    Image.fromarray(array_6).save(pathlib.Path(OUTPUT_DIR) / "6.bmp", 'bmp')
    print("Saved 6.bmp (Brightness-dependent noise, strong)")

    # Image 7: Spatially non-stationary noise, variance depends on COORDINATES (Weak effect, max_var=100)
    array_7 = add_coordinate_dependent_noise(original_array, max_variance=100.0)
    Image.fromarray(array_7).save(pathlib.Path(OUTPUT_DIR) / "7.bmp", 'bmp')
    print("Saved 7.bmp (Coordinate-dependent noise, weak)")

    # Image 8: Spatially non-stationary noise, variance depends on COORDINATES (Strong effect, max_var=300)
    array_8 = add_coordinate_dependent_noise(original_array, max_variance=300.0)
    Image.fromarray(array_8).save(pathlib.Path(OUTPUT_DIR) / "8.bmp", 'bmp')
    print("Saved 8.bmp (Coordinate-dependent noise, strong)")

    print(f"\nSuccessfully generated 9 images in folder: {OUTPUT_DIR}")


if __name__ == "__main__":
    generate_images()