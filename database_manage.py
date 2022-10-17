from src import dbo
import os
from PIL import Image


def scan_path():
    # get all files in path
    os_files = set(os.listdir())
    # get all files in database
    db_files = set([i[0][4:] for i in dbo.search()])
    # get files to add
    add_files = os_files.difference(db_files)
    # get files to remove
    remove_files = db_files.difference(os_files)
    if len(add_files) == 0 and len(remove_files) == 0:
        print("No changes detected")
    else:
        # add files
        for file in add_files:
            # get image size
            img = Image.open(file)
            img_x, img_y = img.size
            # get image name
            name = file.split(".")[0]
            # get image type
            type = input("Enter type for %s (supported type: acg, wallpaper, avatar): " % name)
            # get image format
            format = file.split(".")[1]
            # get image path
            path = "img/" + file
            # insert into database
            dbo.insert(name, type, format, path, img_x, img_y)
            print("Added %s" % file)
        # remove files
        for file in remove_files:
            # get image path
            path = "img/" + file
            # remove from database
            dbo.delete(path)
            print("Removed %s" % file)
