import sqlite3
import os

# connect to database
database = sqlite3.connect("img_info.sqlite3")
# create cursor
cursor = database.cursor()


# initialize database
def init():
    # create table if not exists
    try:
        cursor.execute("CREATE TABLE img (ID VARCHAR 255, NAME text, TYPE text, FORMAT text, img_x int, img_y int)")
        database.commit()
        print("Table created")
    except sqlite3.OperationalError:
        print("Table already exists")


def get_ID():
    try:
        ID = cursor.execute("SELECT ID FROM img").fetchall()
        print(ID)
        return ID
    except sqlite3.OperationalError as e:
        print("Error: %s" % e)
        return {"Error": e}, 500


def insert_img(img):
    try:
        cursor.execute("INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)",
                       (img.ID, img.name, img.type, img.format, img.img_x, img.img_y))
        database.commit()
        print("Added %s" % img.name)
    except sqlite3.OperationalError as e:
        print("Error: %s" % e)
        return {"Error": e}, 500


def delete_img(img):
    try:
        cursor.execute("DELETE FROM img WHERE ID = ?", (img.ID,))
        database.commit()
        print("Removed %s" % img.name)
    except sqlite3.OperationalError as e:
        print("Error: %s" % e)
        return {"Error": e}, 500
