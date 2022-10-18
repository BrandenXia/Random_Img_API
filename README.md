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

## Image download

```shell
python get_img.py
```

### Usage
```shell
python get_img.py <options>
```
Options:
- `--acg`: Get good images
- `--avatar`: Get avatars
- `--help`: Show this message
- `--wallpaper`: Get wallpaper

## Todo
- [ ] Add more download source
- [ ] Add more available parameters
- [ ] modulize