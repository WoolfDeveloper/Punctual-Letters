# Packaging Punctual Letters:

## Table of contents
- [Liberaries used for package the project](#liberaries-used-for-package-the-project)
- [Commands to package the project](#commands-to-package-the-project)
  - [Getting the path of the customtkinter library](#getting-the-path-of-the-customtkinter-library)
  - [Throwing the command to package the project](#throwing-the-command-to-package-the-project)
- [Possible errors](#possible-errors)
    - [Not recognize pyinstaller as a command](#not-recognize-pyinstaller-as-a-command)
    - ['win32ctypes.pywin32.pywintypes.error'](#win32ctypespywin32pywintypeserror)


## Liberaries used for package the project

- PyInstaller
```sh { closeTerminalOnSuccess=false }
pip install pyinstaller
```

- customtkinter
```sh { closeTerminalOnSuccess=false }
pip install customtkinter
```

## Commands to package the project

For package this project is necessary to add customtkinter in the command line, this is because the customtkinter is not a standard library and the pyinstaller does not recognize it.

### Getting the path of the customtkinter library

The command you should use is this:  
```sh { closeTerminalOnSuccess=false }
pip show customtkinter
```

The output of this command should be something like this:  
```sh { closeTerminalOnSuccess=false }
Name: customtkinter
Version: 5.2.2
Summary: Create modern looking GUIs with Python   
Home-page: https://customtkinter.tomschimansky.com
Author: Tom Schimansky
Author-email: 
License: Creative Commons Zero v1.0 Universal     
Location: C:\Users\<USER>\AppData\Local\Packages\PythonVersion\LocalCache\local-packages\Python311\site-packages   
Requires: darkdetect, packaging
Required-by:
```

The path that you should use is the one that is in the `Location` field. The path maybe different in your case.

### Throwing the command to package the project

When you have the path of the customtkinter library you must add an argument to the command that you are going to use to package the project. The argument is `--add-data` and the value of this argument is the path of the customtkinter library and the path where you want to copy the library in the packaged project. The command should look like this:  
```sh { closeTerminalOnSuccess=false }
pyinstaller --ico=./assets/icon.png --noconfirm --onedir --windowed --add-data "<Path of the customtkinter library>;customtkinter/"  ./init.py
```


## Possible errors
### Not recognize pyinstaller as a command

You can use the following command to use pyinstaller:  
```sh { closeTerminalOnSuccess=false }
python -m PyInstaller --ico=./assets/icon.png --noconfirm --onedir --windowed --add-data "<Path of the customtkinter library>;customtkinter/"  ./init.py
```

### 'win32ctypes.pywin32.pywintypes.error'

If when packaging you get this error:  
```sh { closeTerminalOnSuccess=false }
**win32ctypes.pywin32.pywintypes.error: (225, 'BeginUpdateResourceW', 'Operation did not complete successfully because the file contains a virus or potentially unwanted software.')**
```
The latest version sometimes throws this error, you can use the following command to install the previous version:  
```sh { closeTerminalOnSuccess=false }
pip install pyinstaller==5.13.2
```

Using this version the error should not appear.

Reference: [Stack overflow: *win32ctypes.pywin32.pywintypes.error when using pyinstaller in VS Code - Possible Virus/Trojan?](https://stackoverflow.com/questions/77239487/win32ctypes-pywin32-pywintypes-error-when-using-pyinstaller-in-vs-code-possib)
