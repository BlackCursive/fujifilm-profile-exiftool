
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
# Fujifilm Model - Exiftool

Python script that interacts with the command line interface (CLI) to change the camera model on Fujifilm cameras ( especially older models ) to an X-T4
so the following simulations can be used:
* ACROS
* ETERNA
* SEPIA
* BLEACH BYPASS
* CLASSIC NEGATIVE

### Requirements
-- Python 3.6 or higher

-- Exiftool

-- Pandas

-- Tabulate

-- Typer

-------------
### Installation 
#### Check your version of Python and upgrade if necessary
```bash
python3 --version
```

#### Clone repository
```bash
git clone https://github.com/BlackCursive/fujifilm-profile-exiftool.git
cd fujifilm-profile-exiftool
```

### Virtual Environment - Install Pipenv using Homebrew or Python
#### macOS
```bash
brew install pipenv
```
or
#### Python
```bash
pip3 install pipenv
```

### Activate Pipenv Shell
```bash
pipenv shell
```

### Install requirements
```bash
pipenv install -r ./requirements.txt
```
or
```bash
pip3 install pandas
pip3 install tabulate
pip3 install typer
```

### Usage - Be sure to place Fujifilm *.raf files in the raf_files directory or the program will abort
```bash
python3 exifcli.py
```

### Exit Pipenv Shell
```bash
exit
```

---------
## Sample Output
![ExifCli](https://github.com/BlackCursive/fujifilm-profile-exiftool/blob/main/exifcli.gif)


------------------------
This project is built with ![Exiftool](https://github.com/exiftool) by Phil Harvey.
- ExifTool is a platform-independent Perl library plus a command-line application for reading, writing and editing meta information in a wide variety of files.
