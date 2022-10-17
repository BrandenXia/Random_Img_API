# Random_Img_API

A Random Img API build with FastAPI, contain post img and auto download

Project for learning FastAPI.

## Available parameters

- size: [num | ?]x[num | ?]
    - example: 100x100, 100x?, ?x100
    - default: ?x?
- type: [acg | wallpaper | avatar]
    - default: None

## Setup environment

```shell
pip install -r requirements.txt
```

### Run server

```shell
./start.sh
```

### End server

```shell
./end.sh
```

## Database management

```shell
python database_manage.py
```

### Usage

- 1: rescan path, detect file changes and update database
- 2: display database
- 3: exit

## Image download

```shell
python get_img.py
```

### Usage
- 1: acg
- 2: wallpaper [not available yet]
- 3: avatar [not available yet]
- 4: exit

## Todo
- [ ] Add more download source
- [ ] Add more available parameters