import Lab1, Lab2, Lab3, Lab4, Lab5, Lab6


class Menu:
    """
    Handles the user interface and navigation for the terminal-based application.
    It orchestrates calls to the Lab Processors based on user input.
    """

    def __init__(self):
        self.choice = None  # Stores the current user menu choice.
        
        # Initialize Labs cores.
        self.lab1_processor = Lab1.Lab1Processor()
        self.lab2_processor = Lab2.Lab2Processor()
        self.lab3_processor = Lab3.Lab3Processor()
        self.lab4_processor = Lab4.Lab4Processor()
        self.lab5_processor = Lab5.Lab5Processor()
        self.lab6_processor = Lab6.Lab6Processor()

    def main_menu(self):
        print("\nWhich lab you want to run?")
        print("1. Lab 1 (Basic Manipulations)")
        print("2. Lab 2 (Advanced Manipulations)")
        print("3. Lab 3 (Watermark & Slideshow)")
        print("4. Lab 4 (Analysis & Conversion)")
        print("5. Lab 5 (Filtering & Edge Detection)")
        print("6. Lab 6 (Noise Reduction Analysis)")
        print("0. Exit program")
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
            case '5':
                self.lab5_menu()
            case '6':  # <--- Обробка вибору
                self.lab6_menu()
            case '0':
                return
            case _:
                print("Wrong command, try again.")
                self.main_menu()

    def lab1_menu(self):
        print("\n--- Lab 1 Menu ---")
        print("1. Convert image format")
        print("2. Convert image size")
        print("3. Convert colors")
        print("4. Color correction")
        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.lab1_processor.convert_image_format()
                if self.continue_prompt(): self.lab1_menu()
            case '2':
                self.size_menu()
                if self.continue_prompt(): self.main_menu()
            case '3':
                self.lab1_processor.convert_image_color()
                if self.continue_prompt(): self.main_menu()
            case '4':
                self.color_balance_menu()
                if self.continue_prompt(): self.main_menu()
            case _:
                print("Wrong command, try again.")
                self.lab1_menu()

    def size_menu(self):
        print(f"\n--- Resize Menu ---")
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
        print(f"\n--- Color Balance Menu ---")
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
        print("\n--- Lab 2 Menu ---")
        print("1. Change transparency")
        print("2. Crop image")
        print("3. Change contrast")
        self.choice = input('Input your choice: ')
        match self.choice:
            case '1':
                self.lab2_processor.add_transparency()
                if self.continue_prompt(): self.main_menu()
            case '2':
                self.crop_menu()
                if self.continue_prompt(): self.main_menu()
            case '3':
                self.lab2_processor.enhance_contrast()
                if self.continue_prompt(): self.main_menu()
            case _:
                print("Wrong command")
                self.main_menu()

    def crop_menu(self):
        print("\n--- Crop Menu ---")
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
        print("\n--- Lab 3 Menu ---")
        print("1. Combine images")
        print("2. Add watermark")
        print("3. Create slideshow")
        self.choice = input('Input your choice: ')
        match self.choice:
            case '1':
                self.lab3_processor.combine_images()
                if self.continue_prompt(): self.main_menu()
            case '2':
                self.lab3_processor.add_watermark()
                if self.continue_prompt(): self.main_menu()
            case '3':
                self.lab3_processor.create_slideshow()
                if self.continue_prompt(): self.main_menu()
            case _:
                print("Wrong command")
                self.main_menu()

    def lab4_menu(self):
        print("\n--- Lab 4: Image Analysis & Simple Conversion ---")
        print("1. Show Image(s)")
        print("2. Show Brightness Matrix")
        print("3. Show Color Histogram")
        print("4. Binarize Image (Black & White)")
        print("5. Convert to Grayscale")
        print("6. Invert Image (Negative)")
        print("7. Show Grayscale Histogram")
        print("0. Back to Main Menu")
        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.lab4_processor.show_images()
                if self.continue_prompt(): self.main_menu()
            case '2':
                self.lab4_processor.show_brightness_matrix()
                if self.continue_prompt(): self.main_menu()
            case '3':
                self.lab4_processor.show_color_histogram()
                if self.continue_prompt(): self.main_menu()
            case '4':
                self.lab4_processor.binarize_image()
                if self.continue_prompt(): self.main_menu()
            case '5':
                self.lab4_processor.convert_to_grayscale()
                if self.continue_prompt(): self.main_menu()
            case '6':
                self.lab4_processor.invert_image()
                if self.continue_prompt(): self.main_menu()
            case '7':
                self.lab4_processor.show_grayscale_histogram()
                if self.continue_prompt(): self.main_menu()
            case '0':
                self.main_menu()
            case _:
                print("Wrong command, try again.")
                self.lab4_menu()

    def lab5_menu(self):
        print("\n--- Lab 5: Filtering & Edge Detection ---")
        print("1. Roberts Edge Detection (Variant 29->5)")
        print("0. Back to Main Menu")
        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.lab5_processor.roberts_edge_detection()
                if self.continue_prompt(): self.main_menu()
            case '0':
                self.main_menu()
            case _:
                print("Wrong command, try again.")
                self.lab5_menu()

    def continue_prompt(self):
        """Helper to ask for continuation"""
        choice = input("continue (Y/N):").upper()
        return choice == 'Y'


    def lab6_menu(self):
        print("\n--- Lab 6: Noise Reduction Analysis ---")
        print("1. Run Filter Analysis (Linear & Non-Linear MSE)")
        print("0. Back to Main Menu")
        self.choice = input('Input your choice: ')

        match self.choice:
            case '1':
                self.lab6_processor.run_analysis()
                if self.continue_prompt(): self.main_menu()
            case '0':
                self.main_menu()
            case _:
                print("Wrong command, try again.")
                self.lab6_menu()