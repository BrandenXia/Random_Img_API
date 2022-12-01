# Random_Img_API

A Random Img API build with FastAPI, contain post img and auto download

Project for learning.

## Available parameters

- size: `[positive integer or ?]x[positive integer or ?]`
    - example: `100x100`, `100x?`, `?x100`
    - default: `?x?`
- type: `acg` or `wallpaper` or `avatar`
    - example: `acg`, `wallpaper`, `avatar`
    - default: `None`
- rt: `img` or `json`
    - example: `img`, `json`
    - default: `img`

## Setup environment

```shell
pip install random_img_api
```

## Run server

```shell
img_api run <options>
```

### Options
- `--port` `INTEGER`
  - Port to run on
  - default: `8045`
- `--threads` `INTEGER`
  - Number of threads to run
  - default: `2`
- `--workers` `INTEGER`
  - Number of workers to run
  - default: `cpu_count() * 2 + 1`
- `--help`
  - Show help message and exit

## Image download [Not complete yet]

```shell
img_api get <options>
```

### Options
- `--type` / `-t` `TEXT`
  - the type of image to download
  - default: `acg`
  - choices: `acg`, `wallpaper`, `avatar`
- `--num` / `-n`
  - the number of images to download, 0 for unlimited
  - default: `0`
- `--help`
  - Show the help message and exit


## Config

### Change Config

```shell
img_api config <option> <CONFIG_VALUE>
```

Options:
- `--setup` setup config file

Argument:
- `CONFIG_VALUE` allow argument like `img_path=img` or `database_name`

### Database
- `database_name`: Name of database file
  - stored in `config.json`
  - default: `img_info.sqlite3`

### Download
- `img_path`: Path of img folder
  - stored in `config.json`
  - default: `./img`

### Log
- `log_level`: Level of log
  - stored in `config.json`
  - default: `INFO`
  - choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

## Todo
- [ ] Add more available parameters
- [x] Modulize the code
  - [x] allow user to config
    - [x] read and write config file
    - [x] change download path
    - [x] change download source
    - [x] change database path
    - [x] change config using command line
  - [x] change structure of image download
- [x] make a download progress bar with rich
- [ ] use ai to generate images
- [x] add colored log
- [x] add more comments
- [ ] add rsa protection or protection according to ip
- [ ] change return url so that people will be able to review what they just look at
- [x] using setuptools to manage dependencies and build a package
- [x] finish download and generate image function
  - [x] download acg
  - [x] download wallpaper
  - [x] generate avatar
- [x] format commit message