import dropbox
import re

def validate_input(in_str):
    # Check if the string contains only alphabets, numbers, spaces, hyphens and underscores
    if bool(re.match("^[a-zA-Z0-9 _-]*$", in_str)):
        return True
    else:
        return False

def list_folders(dbx, folder_path):
    try:
        response = dbx.files_list_folder(folder_path)
        return [entry for entry in response.entries if isinstance(entry, dropbox.files.FolderMetadata)]

    except Exception as e:
        print(e)
        return []

def main():
    dbx = dropbox.Dropbox('<ACCESS_TOKEN>')
  
    folder_path = input("Enter the path of the root directory you want to start from: ")
    folders_to_evaluate = []
    
    while True:
        folders_in_path = list_folders(dbx, folder_path)

        print(f"\nFolders in {folder_path}:")
        for i, folder in enumerate(folders_in_path):
            print(f"{i+1}. {folder.name}")
        
        selected = input("Enter the number of the sub-folder you want to open (or 'q' to exit): ")
        if selected.lower() == 'q':
            break
        
        if selected.isdigit() and 1 <= int(selected) <= len(folders_in_path):
            idx = int(selected) - 1
            folder_path = folders_in_path[idx].path_lower
            
            add_to_list = input(f"Do you want to add {folders_in_path[idx].name} to the evaluation list? (y/n): ")
            if add_to_list.lower() == 'y':
                folders_to_evaluate.append(folders_in_path[idx])
        
    print("\nFolders added for evaluation:")
    for folder in folders_to_evaluate:
        print(folder.name)

if __name__ == "__main__":
    main()