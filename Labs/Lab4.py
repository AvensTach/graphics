from PIL import Image, ImageOps
import numpy as np
import matplotlib.pyplot as plt
from Common import Service
import pathlib


class Lab4Processor:
    """
    Клас для операцій аналізу зображень та простих перетворень
    (Лабораторна 4).
    """

    def __init__(self):
        self.service = Service()

    def show_images(self):
        """
        Завдання 1: Виведення первинного кольорового зображення на екран.
        """
        files = self.service.get_images()
        if not files:
            print("Файли не вибрано.")
            return

        print(f"Показ {len(files)} зображень...")
        for i in files:
            try:
                img = Image.open(i)
                # .show() відкриває зображення у стандартному переглядачі
                img.show(title=pathlib.Path(i).name)
            except Exception as e:
                print(f"Не вдалося відкрити {i}: {e}")

    def show_brightness_matrix(self):
        """
        Завдання 2: Виведення на екран матриці значень яскравості.
        """
        files = self.service.get_images()
        if not files:
            print("Файли не вибрано.")
            return

        for i in files:
            try:
                img = Image.open(i)
                # Конвертуємо в градації сірого ('L' - luminance)
                grayscale_img = img.convert('L')

                # Конвертуємо зображення в матрицю NumPy
                brightness_matrix = np.array(grayscale_img)

                print(f"\n--- Матриця яскравості для {pathlib.Path(i).name} ---")
                # np.set_printoptions(threshold=np.inf) # Виключає обмеження виводу
                print(brightness_matrix)

            except Exception as e:
                print(f"Не вдалося обробити {i}: {e}")

    def show_color_histogram(self):
        """
        Завдання 3: Побудова гістограми яскравості кольорового зображення.
        """
        files = self.service.get_images()
        if not files:
            print("Файли не вибрано.")
            return

        for i in files:
            try:
                img = Image.open(i)
                # Переконуємося, що зображення в RGB, щоб розділити канали
                rgb_img = img.convert('RGB')

                # .histogram() повертає список з 256 значень для кожного каналу
                # Ми розділяємо канали, щоб отримати 3 окремі гістограми
                r_hist = rgb_img.getchannel('R').histogram()
                g_hist = rgb_img.getchannel('G').histogram()
                b_hist = rgb_img.getchannel('B').histogram()

                plt.figure(figsize=(10, 6))
                plt.title(f'Кольорова гістограма для {pathlib.Path(i).name}')
                plt.plot(r_hist, color='red', alpha=0.7, label='Red')
                plt.plot(g_hist, color='green', alpha=0.7, label='Green')
                plt.plot(b_hist, color='blue', alpha=0.7, label='Blue')
                plt.xlabel('Значення пікселя')
                plt.ylabel('Частота')
                plt.legend()
                plt.grid(True)
                plt.show()  # Відкриває вікно Matplotlib з графіком

            except Exception as e:
                print(f"Не вдалося побудувати гістограму для {i}: {e}")

    def show_grayscale_histogram(self):
        """
        Завдання 4 (частково): Побудова гістограми в градаціях сірого.
        """
        files = self.service.get_images()
        if not files:
            print("Файли не вибрано.")
            return

        for i in files:
            try:
                img = Image.open(i)
                grayscale_img = img.convert('L')

                # .histogram() для 'L' режиму повертає одну гістограму
                grayscale_hist = grayscale_img.histogram()

                plt.figure(figsize=(10, 6))
                plt.title(f'Гістограма в градаціях сірого для {pathlib.Path(i).name}')
                plt.plot(grayscale_hist, color='black')
                plt.xlabel('Значення яскравості (0-255)')
                plt.ylabel('Частота')
                plt.fill_between(range(256), grayscale_hist, color='gray', alpha=0.5)
                plt.grid(True)
                plt.show()

            except Exception as e:
                print(f"Не вдалося побудувати гістограму для {i}: {e}")

    def convert_to_grayscale(self):
        """
        Завдання 4: Перехід до відтінків сірого.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()
        if not files or not output_dir:
            return

        for i in files:
            try:
                img = Image.open(i)
                grayscale_img = img.convert('L')

                filename = pathlib.Path(i).stem + "_grayscale" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                grayscale_img.save(output_path)
                print(f"Збережено в градаціях сірого: {filename}")

            except Exception as e:
                print(f"Не вдалося конвертувати {i}: {e}")

    def invert_image(self):
        """
        Завдання 4: Негатив.
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()
        if not files or not output_dir:
            return

        for i in files:
            try:
                img = Image.open(i)
                # Invert працює коректно з RGB
                rgb_img = img.convert('RGB')

                inverted_img = ImageOps.invert(rgb_img)

                filename = pathlib.Path(i).stem + "_inverted" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                inverted_img.save(output_path)
                print(f"Збережено негатив: {filename}")

            except Exception as e:
                print(f"Не вдалося інвертувати {i}: {e}")

    def binarize_image(self):
        """
        Завдання 4: Бінаризація (чорно-біле).
        """
        files = self.service.get_images()
        output_dir = self.service.get_output_dir()
        if not files or not output_dir:
            return

        try:
            # Запитуємо у користувача поріг
            threshold = int(input("Введіть поріг бінаризації (0-255, за замовчуванням 128): ") or 128)
            if not 0 <= threshold <= 255:
                raise ValueError
        except ValueError:
            print("Некоректне значення. Використано поріг 128.")
            threshold = 128

        for i in files:
            try:
                img = Image.open(i)
                grayscale_img = img.convert('L')

                # Використовуємо .point() для застосування порогу
                # '1' - режим 1-бітного зображення (чорний або білий)
                binarized_img = grayscale_img.point(lambda p: 255 if p > threshold else 0, '1')

                filename = pathlib.Path(i).stem + "_binarized" + ".png"
                output_path = pathlib.Path(output_dir) / filename
                binarized_img.save(output_path)
                print(f"Збережено бінаризоване зображення: {filename}")

            except Exception as e:
                print(f"Не вдалося бінаризувати {i}: {e}")