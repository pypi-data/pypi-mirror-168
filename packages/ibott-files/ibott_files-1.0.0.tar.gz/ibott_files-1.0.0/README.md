## [Files, Folders, Images and PDFs](files_and_folders)

This Python package contains 4 different classes to work with files, folder, images and pdfs in your python developements
for more information about how to develop your RPA projects with python check https://ibott.io/academy

### [1. files.py](files_and_folders/files.py) 
Class to handle files.
Arguments:
1. file_path (str): path to the file

Attributes:
1. file_path (str): path to the file
2. exists (bool): whether the file exists
3. file_name (str): name of the file
4. byte_size (int): size of the file in bytes
5. creation_datetime (datetime): datetime of the file's creation
6. modification_datetime (datetime): datetime of the file's last modification

Methods:
1. rename(new_file_name): renames the file 
2. move(new_location): moves the file to a new location 
3. remove(): removes the file 
4. copy(new_location): copies the file to a new location 
5. wait_for_file_to_exist(timeout=10): waits for the file to exist


### [2. folders.py](files_and_folders/folders.py) 
Class to handle folders. 
If folder doesn't exist it automatically creates a new one.
Arguments:
1. path (str) -- path to folder to be instanced.

Attributes:
1. path (str) -- path to folder to be instanced.
2. name (str) -- name of folder
    
Methods:
1. rename(new_folder_name) : Rename folder 
2. move(new_location): move folder to new location 
3. remove(allow_root=False, delete_read_only=True) : remove folder and all files and folders inside 
4. empty(allow_root=False): delete all files and folders in folder, receives allow_root as parameter 
5. copy(new_location=None) : Copy folder to new location 
6. subfolder_list(): list of subfolders 
7. file_list(): list of files in folder 
8. download_file(url, name=None): downloads file from url

### [3. images.py](files_and_folders/images.py) 
Image Class, heritates from File class
Attributes:
1. size {tuple}: size of image
2. format {str}: format of image

Methods:

1. rotate(): rotate image
2. resize(): resize image
3. crop(): crop image
4. mirrorH(): mirror image horizontally
5. mirrorV(): mirror image vertically

### [3. pdfs.py](files_and_folders/pdfs.py) 
PDF Class Heritates from File Class
Arguments:
1. file_path (str): Path of the file

Attributes:
1. file_path (str): Path of the file
2. pages (int): number of pages in the file
3. info (str): info of the file

Methods:
1. read_pages(page_num, encoding=None): Returns a string with the text in the page
2. append(pdf_document2,merge_path): Appends a pdf document to the current document
3. split(): split pdf into several pdfs.