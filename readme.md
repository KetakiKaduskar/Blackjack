### This is a Blackjack game made with Python's module TKinter
<br/>

- <ins>Steps to get executable file:</ins>
  
  1.   In VSCode Terminal, _pip install pipenv_ for path of project folder
    
  2.   _pipenv install_ required modules (pillow, tkinter, random, pyinstaller)
    
  3.   _pipenv shell_ (When you run _pipenv shell_, it activates the virtual environment associated with your project. Activating the virtual environment sets up your shell session so that when you run Python-related commands, they will use the packages installed within that virtual environment rather than the global Python environment.)
  
  4.  _pyinstaller --onedir --contents-directory "." app.py --add-data "package;package"_

<br/>

#### <ins>_pyinstaller --onedir --contents-directory "." app.py --add-data "package;package"_</ins>


This command, is used to create a standalone executable from a Python script.

- **--onedir:**  This option tells PyInstaller to create a single directory containing all the necessary files for the executable.

- **--contents-directory ".":**  This option specifies the directory from which to copy all necessary files into the output directory. In this case, ***'.'*** represents the current directory.

- **--add-data "package;package":**  This option allows you to add additional data files or directories to the executable. The syntax ***"source;destination"*** specifies that the file or directory at ***'source'*** should be included in the executable and placed at ***'destination'*** within the executable's directory structure. In this case, the ***'package'*** directory and its contents had to be included, and placed in the same relative location within the executable's directory structure.

<br/>

**Video:** https://youtu.be/fgQepqF1R6w
