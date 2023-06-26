import cv2
import os
from glob import glob

folders = []


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
    prompt = "Please choose an option (1-4): "
    while True:
        try:
            option = int(input_validation(prompt))
            if option in [1, 2, 3, 4]:
                return option
            else:
                print("Please choose between options 1 to 4.")
        except:
            print("Invalid input. Please try again.")


def search_folders():
    """Search for folder name"""
    print()
    print("What folder did you want to search for?")
    while True:
        folder_name = input_validation("Folder name: ", validate_folder_name)
        if folder_name is None:
            print("Invalid input. Please try again.")
            continue
        print("Validated folder name:", folder_name)
        
        confirm = input_validation(
            "Confirm? (y/n): ", lambda x: x.lower() in ["y", "yes", "n", "no"]
        )
        if confirm is None:
            print("Invalid input. Please try again.")
            continue
        elif confirm.lower() in ["y", "yes"]:
            folders.append(folder_name)
            print("This is the full list of folders", folders)
            
            add_more = input_validation(
                "Add more folders? (y/n): ", lambda x: x.lower() in ["y", "yes", "n", "no"]
            )
            if add_more is None:
                print("Invalid input. Please try again.")
                continue
            elif add_more.lower() in ["y", "yes"]:
                continue
            else:
                break
        else:
            print("Please try again.")


def check_folders():
    """Check stored folder names"""
    print()
    print("Let's see which folders you have stored!")
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
                    try:
                        folder_name = input_validation(
                            "Please type in the folder that you want to add: ",
                            validate_folder_name,
                        )
                        folders.append(folder_name)
                        add_more = input_validation(
                            "Would you like to add another folder to the list? (y/n): ",
                            lambda x: x.lower() in ["y", "yes", "n", "no"],
                        )
                        if add_more.lower() in ["y", "yes"]:
                            continue
                        else:
                            break
                    except:
                        print("Invalid input. Please try again.")
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
    return


def crop_images():
    """Crop and export images"""
    print()
    confirm_folders = input_validation(
        "Do you want to verify the list of stored folders? (y/n): ",
        lambda x: x.lower() in ["y", "yes", "n", "no"],
    )
    if confirm_folders.lower() in ["y", "yes"]:
        check_folders()
    print(
        "We're getting ready to crop your images! Before we begin, let's make sure everything is set up :)"
    )
    for folder in folders:
        input_folder = folder
        output_folder = "{}_cropped".format(folder)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in glob(os.path.join(input_folder, "*.jpg")):
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
        except:
            print("Error processing image: {}".format(filename))
    print("Image cropping completed successfully!")
    return


def main():
    """Main menu"""
    while True:
        print()
        print("****************************************************************************")
        print("***********************1. Search for folder name ***************************")
        print("***********************2. Check stored folder names ************************")
        print("***********************3. Crop and export images ***************************")
        print("***********************4. Exit *********************************************")
        print("****************************************************************************")
        print()
        option = choose_option()
        if option == 1:
            search_folders()
        elif option == 2:
            check_folders()
        elif option == 3:
            crop_images()
        else:
            exit()


if __name__ == "__main__":
    main()
