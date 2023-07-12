import dropbox

def list_files_in_folder(folder_path):
    dbx = dropbox.Dropbox('<ACCESS_TOKEN>')
    try:
        print('the loop gets in here')
        files = dbx.files_list_folder(folder_path).entries
        for file in files:
            print(file.name)
    except Exception as e:
        print(e)

def main():
   folder_path ="/Mobile Uploads/Photo Shoots Copy/Photo Shoots"
   list_files_in_folder(folder_path)
   exit()


if __name__ == "__main__":
    main()