

This project implements minesweeper and multiple AIs that attempt and, in most cases, succed to solve the board. To run the project, ensure that you are running it from the Minesweeper_112 directory. There are images in the directory that are necessary for the program to run. 

IMPORTANT NOTE: If you use a Macbook Pro with a single button trackpad, Tkinter will not be able to register right clicks. In fact, some wireless mice have had issues with this as well. Use a wired mouse if possible if you are in this situation. Test it on your computer first of course, as this could be a isolated issue for a few computers.

Library installation instructions:

To easily install PIL on Mac OS X 10.7.2 and above,use the following shell commands to download, extract and install the library. Otherwise download the library from the same URL but use the appropriate shell commands.

You will not need to download the PIL library if you run the program from the Minesweeper_112 directory as it can be found inside 
# download
curl -O -L http://effbot.org/downloads/Imaging-1.1.7.tar.gz
# extract
tar -xzf Imaging-1.1.7.tar.gz
cd Imaging-1.1.7
# build and install
python setup.py build
sudo python setup.py install
# or install it for just you without requiring admin permissions:
# python setup.py install --user

Download URL for easyGUI: http://easygui.sourceforge.net/download/version_0.96/index.html

However the easyGUI library is included in this directory. 

To install easyGUI on Windows,open a console window and navigate to wherever your easyGUI folder is (in Minesweeper_112 for example) and enter the following command: python setup.py install.

On a linux or Mac, after you download the file run the following shell command after navigating to the containing directory: python setup.py install.

NOTE: Some forms of Linux may require the use of the sudo command.