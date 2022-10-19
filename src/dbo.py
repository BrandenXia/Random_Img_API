import sqlite3

# connect to database
database = sqlite3.connect("./img_info.sqlite3")
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


def insert(name: str, type: str, format: str, path: str, img_x: int, img_y: int):
    cursor.execute("""INSERT INTO img VALUES (?, ?, ?, ?, ?, ?)""", (name, type, format, path, img_x, img_y))
    database.commit()


def delete(path: str):
    cursor.execute("""DELETE FROM img WHERE PATH = ?""", (path,))
    database.commit()


def search(type: str = None, img_x: int = None, img_y: int = None, needed: str = "*"):
    search_args = []
    if type is not None:
        search_args.append("TYPE = \'%s\'" % type)
    if img_x is not None:
        if img_x != "?":
            search_args.append("img_x = \'%s\'" % img_x)
    if img_y is not None:
        if img_y != "?":
            search_args.append("img_y = \'%s\'" % img_y)
    if len(search_args) == 0:
        res = cursor.execute("SELECT ? FROM img", needed)
    elif len(search_args) == 1:
        res = cursor.execute("SELECT ? FROM img WHERE ?", (needed, search_args[0]))
    else:
        res = cursor.execute("SELECT ? FROM img WHERE ?", (needed, " AND ".join(search_args)))
    return res.fetchall()
