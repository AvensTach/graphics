import Lab1, Lab2, Lab3, Lab4


class Menu:
    """
    Handles the user interface and navigation for the terminal-based application.
    It orchestrates calls to the Lab1Processor based on user input.
    """

    def __init__(self):
        self.choice = None  # Stores the current user menu choice.
        self.lab1_processor = Lab1.Lab1Processor()  # Initialize the image processing core for lab 1.
        self.lab2_processor = Lab2.Lab2Processor()  # Initialize the image processing core for lab 2.
        self.lab3_processor = Lab3.Lab3Processor()  # Initialize the image processing core for lab 3.
        self.lab4_processor = Lab4.Lab4Processor()  # Initialize the image processing core for lab 4.

    def main_menu(self):
        print("\nWhich lab you want to run?")
        print("1. lab 1?")
        print("2. lab 2?")
        print("3. lab 3?")
        print("4. lab 4?")
        print("0. exit program")
        self.choice = input('Input your choice: ')
        match self.choice:
            case '1':
                self.lab1_menu()
            case '2':
                self.lab2_menu()
            case '3':
                self.lab3_menu()
            case '4':
                self.lab4_menu()
            case '0':
                return
            case _:
                print("Wrong command, try again.")
                self.main_menu()

    def lab1_menu(self):
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
                self.lab1_processor.convert_image_format()
                # Prompt to continue or exit.
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.lab1_menu()
            case '2':
                self.size_menu()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '3':
                self.lab1_processor.convert_image_color()
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
                self.lab1_processor.convert_image_size("H")
            case '2':
                self.lab1_processor.convert_image_size("W")
            case '3':
                self.lab1_processor.convert_image_size("HW")
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
                self.lab1_processor.image_color_balance("R")
            case '2':
                self.lab1_processor.image_color_balance("G")
            case '3':
                self.lab1_processor.image_color_balance("B")
            case '4':
                self.lab1_processor.image_color_balance("ALL")
            case _:
                print("Wrong command, try again.")
                self.color_balance_menu()

    def lab2_menu(self):
        print("\nWhat do you want to do?")
        print("1. Change transparency")
        print("2. Crop image")
        print("3. Change contrast")
        self.choice = input('Input your choice: ')
        match self.choice:
            case '1':
                self.lab2_processor.add_transparency()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
                elif self.choice == 'N':
                    return
                else:
                    print("Wrong command")
                    self.main_menu()

            case '2':
                self.crop_menu()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
                elif self.choice == 'N':
                    return
                else:
                    print("Wrong command")
                    self.main_menu()
            case '3':
                self.lab2_processor.enhance_contrast()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
                elif self.choice == 'N':
                    return
                else:
                    print("Wrong command")
                    self.main_menu()
            case _:
                print("Wrong command")
                self.main_menu()

    def crop_menu(self):
        """
        Меню для вибору операції кадрування.
        """
        print("\nChoose action:")
        print("1. Crop")
        print("2. Inverse crop")
        print("3. Slice")

        choice = input("Your choice: ")
        match choice:
            case '1':
                self.lab2_processor.crop_image()
            case '2':
                self.lab2_processor.invert_crop()
            case '3':
                self.lab2_processor.slice_image()
            case _:
                print("Wrong command.")
                self.crop_menu()

    def lab3_menu(self):
        print("\nWhat do you want to do?")
        print("1. Combine images")
        print("2. Add watermark")
        print("3. Create slideshow")
        self.choice = input('Input your choice: ')
        match self.choice:
            case '1':
                self.lab3_processor.combine_images()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
                elif self.choice == 'N':
                    return
                else:
                    print("Wrong command")
                    self.main_menu()

            case '2':
                self.lab3_processor.add_watermark()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
                elif self.choice == 'N':
                    return
                else:
                    print("Wrong command")
                    self.main_menu()
            case '3':
                self.lab3_processor.create_slideshow()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
                elif self.choice == 'N':
                    return
                else:
                    print("Wrong command")
                    self.main_menu()
            case _:
                print("Wrong command")
                self.main_menu()

    def lab4_menu(self):
        print("\nLab 4: Image Analysis & Simple Conversion")
        print("1. Show Image(s)")
        print("2. Show Brightness Matrix")
        print("3. Show Color Histogram")
        print("4. Binarize Image (Чорно-біле)")
        print("5. Convert to Grayscale (Відтінки сірого)")
        print("6. Invert Image (Негатив)")
        print("7. Show Grayscale Histogram")
        print("0. Back to Main Menu")
        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.lab4_processor.show_images()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '2':
                self.lab4_processor.show_brightness_matrix()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '3':
                self.lab4_processor.show_color_histogram()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '4':
                self.lab4_processor.binarize_image()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '5':
                self.lab4_processor.convert_to_grayscale()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '6':
                self.lab4_processor.invert_image()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '7':
                self.lab4_processor.show_grayscale_histogram()
                self.choice = input("continue (Y/N):").upper()
                if self.choice == 'Y':
                    self.main_menu()
            case '0':
                self.main_menu()
            case _:
                print("Wrong command, try again.")
                self.lab4_menu()