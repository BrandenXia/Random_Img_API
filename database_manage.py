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


def manage():
    while True:
        # get user input
        print("\n1. Rescan Path")
        print("2. Search")
        print("3. Exit")
        choice = int(input("Enter choice: "))
        # insert image
        if choice == 1:
            scan_path()
            # search
        elif choice == 2:
            search()
        # exit
        elif choice == 3:
            break
        # invalid input
        else:
            print("Invalid choice")


if __name__ == "__main__":
    # initialize database
    init()
    # manage database
    manage()
    # close database and exit
    cursor.close()
    database.close()
