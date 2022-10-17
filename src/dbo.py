import sqlite3
import os

# connect to database
database = sqlite3.connect("../img_info.sqlite3")
cursor = database.cursor()


# initialize database
def init():
    # create table if not exists
    try:
        cursor.execute("""CREATE TABLE img (NAME text, TYPE text, FORMAT text, PATH text, img_x int, img_y int)""")
        database.commit()
        print("Table created")
    except sqlite3.OperationalError:
        print("Table already exists")
    # change working directory
    os.chdir("./img")


def insert(name: str, type: str, format: str, path: str, img_x: int, img_y: int):
    cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""", (name, type, format, path, img_x, img_y))
    database.commit()


def delete(path: str):
    cursor.execute("""DELETE FROM img WHERE PATH = ?""", (path,))
    database.commit()


def search(type: str = None, img_x: int = None, img_y: int = None):
    search_args = []
    if type is not None:
        search_args.append(f"""TYPE = \'{type}\'""")
    if img_x is not None:
        if img_x != "?":
            search_args.append(f"""img_x = \'{img_x}\'""")
    if img_y is not None:
        if img_y != "?":
            search_args.append(f"""img_y = \'{img_y}\'""")
    print(search_args)
    if len(search_args) == 0:
        print(1)
        res = cursor.execute("SELECT PATH, FORMAT FROM img")
    elif len(search_args) == 1:
        print("SELECT PATH, FORMAT FROM img WHERE %s" % search_args[0])
        res = cursor.execute("SELECT PATH, FORMAT FROM img WHERE %s" % search_args[0])
        print(res.fetchall())
    else:
        print(3)
        res = cursor.execute("SELECT PATH, FORMAT FROM img WHERE %s" % " AND ".join(search_args))
    return res.fetchall()
