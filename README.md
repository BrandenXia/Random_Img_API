# Random_Img_API

A Random Img API build with FastAPI, contain post img and auto download

Project for learning FastAPI.

## Available parameters

- size: `[positive integer | ?]x[positive integer | ?]`
    - example: `100x100`, `100x?`, `?x100`
    - default: `?x?`
- type: `[acg | wallpaper | avatar]`
    - example: `acg`, `wallpaper`, `avatar`
    - default: `None`

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

### Warning
There is a bug that sometimes the program will download images which size is 0 kb when using `--wallpaper` option. 
You can delete these images by using the following command:

```shell
find . -name "*" -type f -size 0c | xargs -n 1 rm -f
```

## Config
### Database
- `database_name`: Name of database file
  - stored in `database.json`
  - default: `img_info.sqlite3`

### Download
- `download_path`: Path of download folder
  - stored in `download.json`
  - default: `./img`

## Todo
- [ ] Add more available parameters
- [ ] Modulize the code
  - [ ] allow user to config
    - [x] read and write config file
    - [x] change download path
    - [ ] change download source
    - [ ] change download format
    - [x] change database path
    - [ ] change config using command line
    - [ ] change database using command line
- [ ] use ai to generate images
- [x] add more comments
- [ ] add rsa protection or protection according to ip
- [ ] change return url so that people will be able to review what they just look at