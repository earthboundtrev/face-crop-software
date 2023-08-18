import cv2
import os
import re
from glob import glob
from tqdm import tqdm 
import time

folders = []

def validate_input(in_str):
    # Check if the string contains only alphabets, numbers, spaces, hyphens and underscores
    if bool(re.match("^[a-zA-Z0-9 _-]*$", in_str)):
        return True
    else:
        return False

def list_folders(folder_path):
    try:
        return [os.path.join(folder_path, name) for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))]
    except Exception as e:
        print(e)
        return []

def retrieve_folder_from_windows():
    folder_path = input("Enter the path of the root directory you want to start from: ")
    
    while True:
        folders_in_path = list_folders(folder_path)

        print(f"\nFolders in {folder_path}:")
        for i, folder in enumerate(folders_in_path):
            print(f"{i+1}. {os.path.basename(folder)}")  # Only print the folder name, not the full path
        
        selected = input("Enter the number of the sub-folder you want to open (or 'q' to exit): ")
        if selected.lower() == 'q':
            main()
        
        if selected.isdigit() and 1 <= int(selected) <= len(folders_in_path):
            idx = int(selected) - 1
            folder_path = folders_in_path[idx]  # Select the new folder path
            
            add_to_list = input(f"Do you want to add {os.path.basename(folders_in_path[idx])} to the evaluation list? (y/n): ")
            if add_to_list.lower() == 'y':
                folders.append(folders_in_path[idx])
    

def pause_screen(seconds):
    """Pause the screen for the specified number of seconds"""
    time.sleep(seconds)

def input_validation(prompt, func=None):
    """Validate user input based on provided function"""
    while True:
        user_input = input(prompt)
        if func is not None and not func(user_input):
            print("Invalid input. Please try again.")
            user_input = None
        return user_input


def validate_folder_name(name):
    """Validate folder name"""
    name = name.strip()
    if name.isalpha():
        return name
    else:
        raise ValueError()


def choose_option():
    """Prompt user for main menu option"""
    print()
    prompt = "Please choose an option (1-5): "
    while True:
        try:
            option = int(input_validation(prompt))
            if option in [1, 2, 3, 4, 5]:
                return option
            else:
                print("Please choose between options 1 to 5.")
        except:
            print("Invalid input. Please try again.")


def print_folders():
    if(len(folders) > 0):
       print("This is the full list of folders to crop the images of:", folders)
    else:
        print("The list of folders to crop the images of is empty! Going back to main menu.")
    

def search_folders():
    """Check stored folder names"""
    print()
    print("Let's see which folders you have stored!")
    if len(folders)== 0:
       print("You have nothing stored! Returning to main menu.")
    if len(folders) > 0:
        print("Folders: ")
        for folder in folders:
            print(folder)
        change_folders = input_validation(
            "Is there anything that you would like to change about this list? (y/n): ",
            lambda x: x.lower() in ["y", "yes", "n", "no"],
        )
        if change_folders.lower() in ["y", "yes"]:
            option = int(
                input_validation(
                    "You would like to change the list! How did you want to change it? Please enter 1 to add, 2 to remove: "
                )
            )
            if option == 1:
                while True:
                    retrieve_folder_from_windows()
            elif option == 2:
                remove_option = int(
                    input_validation(
                        "Did you want to remove something from the list or the entire list? Please enter 1 to remove something or 2 to remove the entire list: "
                    )
                )
                if remove_option == 1:
                    print("Folders: ")
                    for folder in folders:
                        print(folder)
                    remove_folder = input_validation(
                        "Please type in the name of the folder that you don't want on the list anymore: ",
                        validate_folder_name,
                    )
                    if remove_folder in folders:
                        folders.remove(remove_folder)
                    else:
                        print("Folder not found in list.")
                elif remove_option == 2:
                    folders.clear()
                else:
                    print("Please try again.")
            else:
                print("Please enter either 1 or 2.")
    else:
        print(
            "Oh! It looks like the folders are empty! If you want to perform some *magic* on the folders you will need to tell me which ones to work on!"
        )
        print("Going back to main menu.")
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
        crop_eyes_noses()
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
    
    total_files = sum(len(files) for _, _, files in os.walk('.')) - 2  # Excluding current file and directories
    processed_files = 0
    
    for folder in folders:
        input_folder = folder
        output_folder = "{}_cropped".format(folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in tqdm(glob(os.path.join(input_folder, "*.jpg"))):
            try:
                imagePath = filename
                face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                img = cv2.imread(imagePath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                for x, y, w, h in faces:
                    cropped = img[y : y + h, x : x + w]
                    cv2.imshow("cropped", cropped)
                    cv2.waitKey(0)
                    cv2.imwrite(
                        os.path.join(output_folder, os.path.basename(filename)), cropped
                    )
                processed_files += 1
                percentage = int((processed_files / total_files) * 100)
                tqdm.write("Processing: {}%".format(percentage))
            except:
                print("Error processing image: {}".format(filename))
    
    print("Image cropping completed successfully!")

def crop_eyes():
    """Crop and export eyes from images"""
    print("We're getting ready to crop eyes from your images! Before we begin, let's make sure everything is set up :)")
    
    total_files = sum(len(files) for _, _, files in os.walk('.')) - 2  # Excluding current file and directories
    processed_files = 0
    
    for folder in folders:
        input_folder = folder
        output_folder = "{}_cropped_eyes".format(folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")

        for filename in tqdm(glob(os.path.join(input_folder, "*.jpg"))):
            try:
                imagePath = filename
                img = cv2.imread(imagePath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                eyes = eye_cascade.detectMultiScale(gray)
                for x, y, w, h in eyes:
                    cropped = img[y: y + h, x: x + w]
                    cv2.imshow("cropped", cropped)
                    cv2.waitKey(0)
                    cv2.imwrite(os.path.join(output_folder, os.path.basename(filename)), cropped)
                processed_files += 1
                percentage = int((processed_files / total_files) * 100)
                tqdm.write("Processing: {}%".format(percentage))
            except:
                print("Error processing image: {}".format(filename))
    
    print("Image cropping completed successfully!")

def crop_eyes_noses():
    """Crop and export eyes and noses from images"""
    print("We're getting ready to crop eyes and noses from your images! Before we begin, let's make sure everything is set up :)")
    
    total_files = sum(len(files) for _, _, files in os.walk('.')) - 2  # Excluding current file and directories
    processed_files = 0
    
    for folder in folders:
        input_folder = folder
        output_folder = "{}_cropped_eyes_noses".format(folder)

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        eye_cascade = cv2.CascadeClassifier("haarcascade_eye.xml")
        nose_cascade = cv2.CascadeClassifier("haarcascade_mcs_nose.xml")

        for filename in tqdm(glob(os.path.join(input_folder, "*.jpg"))):
            try:
                imagePath = filename
                img = cv2.imread(imagePath)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                eyes = eye_cascade.detectMultiScale(gray)
                noses = nose_cascade.detectMultiScale(gray)

                for x, y, w, h in eyes:
                    cropped = img[y: y + h, x: x + w]
                    cv2.imshow("cropped", cropped)
                    cv2.waitKey(0)
                    cv2.imwrite(os.path.join(output_folder, os.path.basename(filename)), cropped)

                for x, y, w, h in noses:
                    cropped = img[y: y + h, x: x + w]
                    cv2.imshow("cropped", cropped)
                    cv2.waitKey(0)
                    cv2.imwrite(os.path.join(output_folder, os.path.basename(filename)), cropped)
                processed_files += 1
                percentage = int((processed_files / total_files) * 100)
                tqdm.write("Processing: {}%".format(percentage))
            except:
                print("Error processing image: {}".format(filename))
    
    print("Image cropping completed successfully!")

def main():
    """Main menu"""
    while True:
        print()
        print("****************************************************************************")
        print("***********************1. Add folders to be evaluated **********************")
        print("***********************2. Print folder names *******************************")
        print("***********************3. Check stored folder names ************************")
        print("***********************4. Crop and export images ***************************")
        print("***********************5. Exit *********************************************")
        print("****************************************************************************")
        print()
        option = choose_option()
        if option == 1:
            retrieve_folder_from_windows()
        if option == 2:
            print_folders()
        elif option == 3:
            search_folders()
        elif option == 4:
            crop_image_selector()
        else:
            exit()

if __name__ == "__main__":
    main()
