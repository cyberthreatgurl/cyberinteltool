import tarfile
import os
import zipfile
from pathlib import Path

cwd = os.getcwd()
patent_tars_dir = cwd + '/corpus/uspto/'

print('Current Directory:')
print (cwd)

filename = patent_tars_dir + 'I20220811.tar'

file_obj = tarfile.open(filename, 'r')

namelist = file_obj.getnames()

print('files in the tar file:')
#for name in namelist:
#    print(name)
for member in file_obj.getmembers():
    # if a ZIP file, then extract XML files from it.
    filename = Path(member.name).name
    if filename.find('ZIP') != -1:
        # extract the zip file
        zip_file = file_obj.extractfile(member.name)
        # check contents of ZIP file and extract only XML file
        if (zipfile.is_zipfile(zip_file)):
           print (filename)
      #     print file.
    # if file
    # find and extract XML files


    # extract abstract

    # if abstract contains "cyber", print filename and abstract

file_obj.close()

