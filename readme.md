### This is a Blackjack game made with Python's module TKinter
<br/>

- Steps to get executable file:
  
  -  In VSCode Terminal, _pip install pipenv_ for path of project folder
    
  -  _pipenv install_ required modules (pillow, tkinter, random, pyinstaller)
    
  -  _pipenv shell_ (When you run _pipenv shell_, it activates the virtual environment associated with your project. Activating the virtual environment sets up your shell session so that when you run Python-related commands, they will use the packages installed within that virtual environment rather than the global Python environment.)
  
  -  _pyinstaller --onedir --contents-directory "." app.py --add-data "package;package"_
