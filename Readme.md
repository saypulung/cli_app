# CLI Tool

## Overview

This CLI tool provides three main commands to manage and process items in the system:

### Commands

`python main.py cmd-1 --path test --identifier test`

`python main.py cmd-2 --id 1 --filter a`

`python main.py cmd-3 --id 1 --tags test,tast,tost`


### 1 Init

Extract `Installer/CLI-app.app/Contents/Resources/python_env.zip` to `Installer/CLI-app.app/Contents/Resources/python_env`

### 2 Build

`nuitka gui.py --static-libpython=no`

`nuitka main.py --static-libpython=no`

### 3 Prepare Build

`cp gui.bin Installer/CLI-app.app/Contents/MacOS`

`cp main.bin Installer/CLI-app.app/Contents/MacOS`

### 4 Build DMG

`brew install create-dmg`

`cd Installer`

`create-dmg --volname "CLI app" --app-drop-link 600 185 "CLI-app.dmg" CLI-app.app`