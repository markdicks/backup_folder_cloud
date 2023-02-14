import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Authenticate with Google Drive API
gauth = GoogleAuth()
gauth.Auth()

# Get the authenticated GoogleDrive instance
drive = GoogleDrive(gauth)

# Ask user for the directory to back up
folder_path = input("Enter the directory to back up: ")
folder_name = os.path.basename(folder_path)

# Check if the folder already exists in Google Drive
folder_exists = False
file_list = drive.ListFile({'q': "trashed=false and mimeType='application/vnd.google-apps.folder' and title='" + folder_name + "'"}).GetList()
if len(file_list) > 0:
    folder_exists = True
    folder_id = file_list[0]['id']

# Create a new folder in Google Drive if it doesn't exist
if not folder_exists:
    folder = drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
    folder.Upload()
    folder_id = folder['id']
    print("New folder created in Google Drive with ID:", folder_id)

# Upload the directory to Google Drive
folder_file = drive.CreateFile({'title': folder_name, 'parents': [{'id': folder_id}], 'mimeType': 'application/vnd.google-apps.folder'})
folder_file.Upload()

for root, dirs, files in os.walk(folder_path):
    for file in files:
        file_path = os.path.join(root, file)
        file_name = os.path.relpath(file_path, folder_path)
        file_drive_list = drive.ListFile({'q': "trashed=false and mimeType!='application/vnd.google-apps.folder' and title='" + file_name + "' and parents in '" + folder_id + "'"}).GetList()
        if len(file_drive_list) > 0:
            file_drive = file_drive_list[0]
            file_drive.SetContentFile(file_path)
            file_drive.Upload()
            print("Updated file in Google Drive:", file_name)
        else:
            file_drive = drive.CreateFile({'title': file_name, 'parents': [{'id': folder_id}]})
            file_drive.SetContentFile(file_path)
            file_drive.Upload()
            print("Uploaded new file to Google Drive:", file_name)
