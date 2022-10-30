import sqlite3
import os

from random_img_api.src.config import config

# Create database directory if not exists
if not os.path.exists("database"):
    os.makedirs("database")
# read database config
_config = config.Config("config.json")
database_name = _config.get("database_name")
# connect to database
database = sqlite3.connect(os.path.join("database", database_name))
cursor = database.cursor()


# initialize database
def init() -> None:
    """
    initialize database
    """
    # create table if not exists
    try:
        cursor.execute("""CREATE TABLE img (NAME text, TYPE text, FORMAT text, PATH text, img_x int, img_y int)""")
        database.commit()
        print("Table not exist, creating table...")
    except sqlite3.OperationalError:
        return


def insert(name: str, type: str, format: str, path: str, img_x: int, img_y: int) -> None:
    """
    :param name: name of image
    :param type: type of image (acg / wallpaper / avatar)
    :param format: format of image (jpg / png / ...)
    :param path: path of image
    :param img_x: width of image
    :param img_y: height of image
    :return: error message if error occurred, else None
    """
    cursor.execute("INSERT INTO img VALUES ('%s', '%s', '%s', '%s', '%d', '%d')"
                   % (name, type, format, path, img_x, img_y,))
    database.commit()


def delete(path: str) -> None:
    """
    :param path: the path of image to be deleted
    :return: error message if error occurred, else None
    """
    cursor.execute("DELETE FROM img WHERE PATH = '%s'" % (path,))
    database.commit()


def search(type: str = None, img_x: int = None, img_y: int = None, needed: str = "*") -> list:
    """
    :param type: type of image (acg / wallpaper / avatar)
    :param img_x: width of image
    :param img_y: height of image
    :param needed: the column needed to be returned
    :return: error message if error occurred, else the result
    """
    search_args = []
    # add type to search args
    if type is not None:
        search_args.append("TYPE = \'%s\'" % (type,))
    # add img_x to search args
    if img_x is not None:
        if img_x != "?":
            search_args.append("img_x = \'%s\'" % (img_x,))
    # add img_y to search args
    if img_y is not None:
        if img_y != "?":
            search_args.append("img_y = \'%s\'" % (img_y,))
    # if no search args, return all
    if len(search_args) == 0:
        res = cursor.execute("SELECT %s FROM img" % (needed,))
    # if one or more search args, return the search result
    elif len(search_args) == 1:
        res = cursor.execute("SELECT %s FROM img WHERE %s" % (needed, search_args[0],))
    else:
        res = cursor.execute("SELECT %s FROM img WHERE %s" % (needed, " AND ".join(search_args),))
    return res.fetchall()
