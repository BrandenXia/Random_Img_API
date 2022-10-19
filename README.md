# Random_Img_API

A Random Img API build with FastAPI, contain post img and auto download

Project for learning FastAPI.

## Available parameters

- size: [positive integer | ?]x[positive integer | ?]
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
python download_img.py
```

### Usage
```shell
python download_img.py <options>
```
Options:
- `--acg`: Get good images
- `--wallpaper`: Get wallpapers
- `--avatar`: Get avatars
- `--help`: Show this message

## Todo
- [ ] Add more download source
- [ ] Add more available parameters
- [ ] modulize