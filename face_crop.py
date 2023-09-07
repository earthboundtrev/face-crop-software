import argparse
from multiprocessing import Pool
from pydantic import BaseModel, validator
import logging
from pathlib import Path
import os
import cv2
import re
from glob import glob
from tqdm import tqdm 
import time
import numpy as np

folders = []

def validate_input(in_str: str):
    """
    Validates the input string to ensure it contains only alphabets, numbers, spaces, hyphens, and underscores.

    Args:
        in_str (str): The input string to be validated.

    Returns:
        bool: True if the input string is valid, False otherwise.
    """
    return bool(re.fullmatch("^[a-zA-Z0-9 _-]*$", in_str))

def list_folders(folder_path, include_subdirectories=True):
    try:
        if include_subdirectories:
            return [entry.path for entry in os.scandir(folder_path) if entry.is_dir()]
        else:
            return [entry.path for entry in os.scandir(folder_path) if entry.is_dir() and not entry.is_symlink()]
    except Exception as e:
        raise e

def retrieve_folder_from_windows():
    try:
        while True:
            folder_path = input("Enter the path of the root directory you want to start from: ")
            if Path(folder_path).is_dir():
                break
            else:
                print("Invalid directory path. Please try again.")
        
        while True:
            folders_in_path = list_folders(folder_path)

            print_folders(folders_in_path)
            
            selected = input("Enter the number of the sub-folder you want to open (or 'q' to exit): ")
            if selected.lower() == 'q':
                main()
            
            if selected.isdigit() and 1 <= int(selected) <= len(folders_in_path):
                idx = int(selected) - 1
                folder_path = Path(folders_in_path[idx])  # Select the new folder path
                
                add_to_list = input(f"Do you want to add {folder_path.name} to the evaluation list? (y/n): ")
                if add_to_list.lower() == 'y':
                    # Add code to add the folder to the evaluation list
                    pass
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Add code to handle the exception



def print_folders(folders):
    folder_path = Path(folder_path)
    print(f"\nFolders in {folder_path}:")
    for i, folder in enumerate(folders):
        print(f"{i+1}. {folder_path.joinpath(folder).name}")  # Only print the folder name, not the full path
        folders.append(folder_path[i])
    

def pause_screen(seconds: int):
    """Pause the screen for the specified number of seconds"""
    if not isinstance(seconds, int) or seconds <= 0:
        raise ValueError("Seconds must be a positive integer")
    try:
        time.sleep(seconds)
    except Exception as e:
        print(f"An error occurred during the pause: {e}")
        raise ValueError("Seconds must be a positive number")
    try:
        time.sleep(seconds)
    except Exception as e:
        print(f"Error occurred during pause_for_seconds: {e}")
    return "Pause completed"

def input_validation(prompt, func=None, error_message="Invalid input. Please try again."):
    """Validate user input based on provided function"""
    while True:
        user_input = input(prompt)
        if func is not None and not isinstance(func, callable):
            print(error_message)
            user_input = None
        else:
            try:
                if not func(user_input):
                    print(error_message)
                    user_input = None
                else:
                    return user_input
            except:
                print("An error occurred. Please try again.")
        return user_input


def validate_folder_name(name):
    """Validate folder name"""
    name = name.strip()
    if name == "":
        raise ValueError("Folder name cannot be empty")
    elif len(name) > 255:
        raise ValueError("Folder name is too long")
    elif not name.isalnum() and '-' not in name and '_' not in name and ' ' not in name:
        raise ValueError("Folder name must contain only alphanumeric characters, hyphen, underscore, or space")
    return True


def choose_option():
    """Prompt user for main menu option"""
    logging.info("")
    prompt = "Please choose an option (1-6): "
    while True:
        try:
            option = int(input_validation(prompt, func=int, error_message="Please enter a valid integer."))
            if option in range(1, 7):
                return option
            else:
                logging.warning("Please choose between options 1 to 6.")
        except ValueError:
            logging.error("Invalid input. Please try again.")
            print("Invalid input. Please try again.")


def print_folders(folders):
    """
    Prints the list of folders to be used for cropping images.
    
    Args:
    - folders: A list of folders.
    """
    if folders is None or not isinstance(folders, list):
        print("No folders to print.")
    elif len(folders) > 0:
        print(f"This is the full list of folders to crop the images of: {folders}")
    else:
        return None
        print("The list of folders to crop the images of is empty! Going back to main menu.")
  
    
def remove_folders():
    """Remove specified folders based on partial string matches"""
    if len(folders) < 1:
        print("There are no elements in the list! Returning to the main menu.")
        main()

    print("What folder did you want to remove?")
    while True:
        try:
            folder_name = input_validation("Folder name: ", validate_folder_name)
            matching_folders = []

            for folder in folders:
                if folder_name.lower() in folder.lower():
                    matching_folders.append(folder)

            if len(matching_folders) == 0:
                print("No matching folders found.")
            else:
                print("Matching folders:")
                for folder in matching_folders:
                    print(folder)

                confirm = input_validation("Confirm removal? (y/n): ", lambda x: x.lower() in ['y', 'yes', 'n', 'no'])
                if confirm.lower() in ['y', 'yes']:
                    for folder in matching_folders:
                        folders.remove(folder)

            add_more = input_validation("Remove more folders? (y/n): ", lambda x: x.lower() in ['y', 'yes', 'n', 'no'])
            if add_more.lower() in ['y', 'yes']:
                continue
            else:
                break
        except:
            print("Incorrect input was inserted. Please try again.")

    if len(folders) < 1:
        print("There are no elements in the list! Returning to the main menu.")
        main()

        
def get_user_input(prompt):
    """Get user input"""
    return input(prompt)

def validate_user_input(user_input, validation_func):
    """Validate user input"""
    return validation_func(user_input)

def prompt_user_input(prompt, validation_func):
    """Prompt user for input and validate"""
    while True:
        user_input = get_user_input(prompt)
        if validate_user_input(user_input, validation_func):
            return user_input
        else:
            print("Invalid input. Please try again.")


class ChangeFoldersInput(BaseModel):
    change_folders: str

    @validator('change_folders')
    def validate_change_folders(cls, value):
        if value.lower() not in ["y", "yes", "n", "no"]:
            raise ValueError("Invalid input. Please enter 'y', 'yes', 'n', or 'no'.")
        return value

def search_folders():
    """Check stored folder names"""
    logger = logging.getLogger(__name__)
    logger.info("Checking stored folder names")
    try:
        print()
        print("Let's see which folders you have stored!")
        if len(folders) == 0:
            logger.info("You have nothing stored! Returning to main menu.")
        if len(folders) > 0:
            logger.info("Folders: ")
            for folder in folders:
                logger.info(folder)
            change_folders_input = ChangeFoldersInput(change_folders=input("Is there anything that you would like to change about this list? (y/n): "))
            change_folders = change_folders_input.change_folders
            if change_folders.lower() in ["y", "yes"]:
                option = int(
                    prompt_user_input(
                        "You would like to change the list! How did you want to change it? Please enter 1 to add, 2 to remove: ",
                        lambda x: x.isdigit() and int(x) in [1, 2],
                    )
                )
                if option == 1:
                    while True:
                        retrieve_folder_from_windows()
                elif option == 2:
                    remove_option = int(
                        prompt_user_input(
                            "Did you want to remove something from the list or the entire list? Please enter 1 to remove something or 2 to remove the entire list: ",
                            lambda x: x.isdigit() and int(x) in [1, 2],
                        )
                    )
                    if remove_option == 1:
                        logger.info("Folders: ")
                        for folder in folders:
                            logger.info(folder)
                        remove_folder = prompt_user_input(
                            "Please type in the name of the folder that you don't want on the list anymore: ",
                            validate_folder_name,
                        )
                        if remove_folder in folders:
                            folders.remove(remove_folder)
                        else:
                            logger.info("Folder not found in list.")
                    elif remove_option == 2:
                        folders.clear()
                    else:
                        logger.info("Please try again.")
                else:
                    logger.info("Please enter either 1 or 2.")
        else:
            logger.info(
                "Oh! It looks like the folders are empty! If you want to perform some *magic* on the folders you will need to tell me which ones to work on!"
            )
            logger.info("Going back to main menu.")
    except ValueError as ve:
        logger.error(f"An error occurred: {str(ve)}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {str(e)}")
        raise e
    return


def crop_image_selector():
    """Select and perform image cropping based on user's choice"""
    print("Which of the crop functions would you like to use?\n\n" 
          "You can:\n\n"
          "1. Crop all faces out of images.\n"
          "2. Crop all eyes out of images.\n"
          "3. Crop all eyes and noses out of images.\n"
          "4. Exit crop selection and return to the main menu.\n\n"
          "Please select your choice by entering a number between 1 to 4.\n")
  
    crop_choice = input_validation(
        "Enter your choice (1-4): ",
        lambda x: x.isdigit() and 1 <= int(x) <= 4
    )
  
    if crop_choice == "1":
        crop_faces()
    elif crop_choice == "2":
        crop_eyes()
    elif crop_choice == "3":
        #crop_eyes_noses()
        print("Function needs to be refactored/rewritten...")
    elif crop_choice == "4":
        print("Returning to the main menu...")
        return
    else:
        print("Invalid choice. Please select a number between 1 and 4.")
        seconds = 3
        pause_screen(seconds)
        crop_image_selector()
        
        
def crop_faces():
    """Crop and export faces from images"""
    print("We're getting ready to crop faces from your images! Before we begin, let's make sure everything is set up :)")

    relative_path_face_XML = "haarscascade_frontface_default.xml"
    absolute_path = os.path.abspath(relative_path_face_XML)
    face_cascade = cv2.CascadeClassifier(absolute_path)

    for folder in folders:
        output_folder = "{}_cropped_faces".format(folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for processed_files, filename in enumerate(tqdm(glob(os.path.join(folder, "*.jpg"))), start=1):
            try:
                img = cv2.imread(filename)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for x, y, w, h in faces:
                    cropped = img[y : y + h, x : x + w]
                    cv2.imwrite(
                        os.path.join(output_folder, os.path.basename(filename)), cropped
                    )
                tqdm.write("Processing file number: {}".format(processed_files))
            except:
                print("Error processing image: {}".format(filename))
    print("Image cropping completed successfully!")


def crop_eyes(folders):
    """Crop and export eyes from images"""
    logging.basicConfig(level=logging.ERROR)
    logging.info("We're getting ready to crop eyes from your images! Before we begin, let's make sure everything is set up :)")

    processed_files = 0
    eye_cascade = cv2.CascadeClassifier(os.path.abspath("haarscascade_eye.xml"))

    output_folders = ["{}_cropped_eyes".format(folder) for folder in folders if not os.path.exists("{}_cropped_eyes".format(folder))]

    for folder, output_folder in zip(folders, output_folders):
        os.makedirs(output_folder, exist_ok=True)

        for filename in tqdm(glob(os.path.join(folder, "*.jpg"))):
            try:
                img, gray = load_and_convert_image(filename)
                eyes = eye_cascade.detectMultiScale(gray)
                for x, y, w, h in eyes:
                    cropped = img[y: y + h, x: x + w]
                    cv2.imwrite(os.path.join(output_folder, os.path.basename(filename)), cropped)
                processed_files += 1
                tqdm.write("Processing file number: {}".format(processed_files))
            except:
                logging.error("Error processing image: %s", filename)
    print("Image cropping completed successfully!")


def load_and_convert_image(filename):
    img = cv2.imread(str(filename))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img, gray

def process_image(img):
    print("to do")

def process_folder(folder):
    input_folder = folder
    output_folder = "{}_cropped_eyes_noses".format(folder)

    Path(output_folder).mkdir(parents=True, exist_ok=True)

    relative_path_eye_XML = "haarscascade_eye.xml"
    absolute_path_eye = Path().resolve() / relative_path_eye_XML
    eye_cascade = cv2.CascadeClassifier(str(absolute_path_eye))
    relative_path_nose_XML = "haarscascade_mcs_nose.xml"
    absolute_path_nose = Path().resolve() / relative_path_nose_XML
    nose_cascade = cv2.CascadeClassifier(str(absolute_path_nose))

    processed_files = 0
    for filename in tqdm(Path(input_folder).glob("*.jpg")):
        try:
            img, gray = load_and_convert_image(filename)
            eyes, noses = process_image(img)

            for i, (x, y, w, h) in enumerate(eyes):
                cropped = img[y: y + h, x: x + w]
                output_path = Path(output_folder) / (Path(filename).stem + f"_eye_{i}" + Path(filename).suffix)
                cv2.imwrite(str(output_path), cropped)

            for i, (x, y, w, h) in enumerate(noses):
                cropped = img[y: y + h, x: x + w]
                output_path = Path(output_folder) / (Path(filename).stem + f"_nose_{i}" + Path(filename).suffix)
                cv2.imwrite(str(output_path), cropped)
            processed_files += 1
            tqdm.write("Processing file number: {}".format(processed_files))
        except Exception as e:
            logging.exception("Error processing image: {}".format(filename), exc_info=e)

if __name__ == "__main__":
    with Pool() as pool:
        pool.map(process_folder, folders)
    print("Image cropping completed successfully!")

def main():
    """Main menu"""
    parser = argparse.ArgumentParser(description="Image cropping tool")
    parser.add_argument("option", type=int, choices=range(1, 7), help="Choose an option (1-6)")
    args = parser.parse_args()

    option_functions = {
        1: retrieve_folder_from_windows,
        2: remove_folders,
        3: print_folders,
        4: search_folders,
        5: crop_image_selector,
        6: exit
    }

    try:
        option = args.option
        if option in option_functions:
            option_functions[option]()
        else:
            print("Invalid option. Please choose a number between 1 and 6.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
