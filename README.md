# BingDailyWallpaper

## Description

A simple tool to collect wallpapers from bing.com

## How To Use

 - Linux
   - git clone this repository
   - excute "pip install -r requirements.txt"
   - excute "bash run.sh"

 - Windows
   - open cmd
   - git clone this repository
   - excute "pip install -r requirements.txt"
   - excute "pyinstaller -F Win32Service.py"
   - excute "dist\Win32Service.exe install && dist\Win32Service.exe update && dist\Win32Service.exe start"

- Docker
  - install docker
  - ```docker run -d -v you image dir:/images dengzhenzhen/bing-daily-wallpaper:0.0.1```

## Todo List

 - ~~Add method how to deploy on Windows~~(Done)
 - ~~E-mail notice~~(Done)
 - ~~Auto install shell script~~(Done)
