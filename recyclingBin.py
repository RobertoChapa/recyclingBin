# Bobby Chapa
# 6/21/2021

import os
from winreg import *  # Edit
import time

def main():
    recycledDir = returnDir() # returns the correct Recycle directory
    findRecycled(recycledDir)

def returnDir():
    dirs = ['C:\\Recycler\\', 'C:\\Recycled\\', 'C:\\$Recycle.Bin\\']

    for recycleDir in dirs:
        if os.path.isdir(recycleDir):
            return recycleDir
    return None

def sid2user(sid):
    try:
        key = OpenKey(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\ProfileList" + '\\' + sid)
        (value, type) = QueryValueEx(key, 'ProfileImagePath')
        user = value.split('\\')[-1]

        return user
    except:
        return sid

# retrieves files that begin $I from the recycle.Bin directory.
# called from findRecycled()
def get_I_File_Info(file,recycleDir):
    if file[1] == "I":
        full_path = recycleDir

        deleted_file_content = open(full_path, 'r', encoding="cp850")
        deleted_file_path = deleted_file_content.read()
        deleted_file_content.close()

        deleted_file_path = deleted_file_path[28:]
        string_length = len(deleted_file_path)
        deleted_file_path_parsed = ""

        x = 0

        while x < string_length:
            deleted_file_path_parsed += deleted_file_path[x]

            x += 2

        filename = deleted_file_path_parsed.rsplit('\\', 1)[-1]
    else:
        filename =''
        # do nothing

    return filename

# retrieve deleted file meta data
def findRecycled(recycleDir):
    dirList = os.listdir(recycleDir)

    for sid in dirList:
        files = os.listdir(recycleDir + sid)
        user = sid2user(sid)

        print('\n[*] Listing Files for User: ' + str(user))  # Edit

        input() # pause between user

        for file in files:
            fileName = get_I_File_Info(file, recycleDir+sid+"\\"+file)

            if fileName: # $I files were returned retrieve file meta data
                creation_time = os.path.getctime(recycleDir+sid+"\\"+file)
                creation_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))

                modified_time = os.path.getmtime(recycleDir+sid+"\\"+file)
                modified_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modified_time))

                access_time = os.path.getatime(recycleDir+sid+"\\"+file)
                access_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(access_time))

                # get $R file for the $I file that we are examining to determine size
                try:
                    r_filename = "$R" + file[2:]
                    file_size = str(os.path.getsize(recycleDir+sid+"\\"+r_filename))
                except:
                    file_size = '{0} was not found'.format(r_filename)

                print()
                print('[+] Found File: ' + str(file) + ' ')
                print('Original File Name ' + fileName)
                print('File Size: ', file_size)
                print('Creation Time ' + creation_time + ' DELETION DATE ')
                print('Modification Time ' + modified_time+ ', ')
                print('Access_time: ' + access_time + ', ')
                print()

            else: # no $I files were returned
                fileName = ''
                # do nothing
    return


if __name__ == '__main__':
    main()