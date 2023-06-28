import dropbox

def list_files_in_folder(folder_path):
    dbx = dropbox.Dropbox('<ACCESS_TOKEN>')
    try:
        files = dbx.files_list_folder(folder_path).entries
        for file in files:
            print(file.name)
    except Exception as e:
        print(e)
        """
        To get the folder path for a Dropbox folder, you can follow these steps:

Go to the Dropbox website and sign in to your account.
Navigate to the folder you want to access.
Click on the folder to open it.
Look at the URL in your web browser’s address bar. The folder path will be the part of the URL that comes after https://www.dropbox.com/home.
For example, if the URL is https://www.dropbox.com/home/my_folder, then the folder path is /my_folder.

I hope this helps! Let me know if you have any other questions.
        """
        
"""       

       import cv2
import glob

def faceCrop(imagePath):
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    img = cv2.imread(imagePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cropped = img[y:y+h, x:x+w]
        cv2.imshow("cropped", cropped)
        cv2.waitKey(0)

faceCrop('test.jpg')

import os
import facecrop

input_folder = './input_folder'
output_folder = './output_folder'

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for filename in os.listdir(input_folder):
    if filename.endswith('.jpg'):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        facecrop.crop(input_path, output_path, "image/jpeg", 0.95, 1.5)
        """