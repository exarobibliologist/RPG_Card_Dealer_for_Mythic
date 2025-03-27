# RPG_Card_Dealer_for_Mythic

![Made For Mythic Cards](https://i.imgur.com/1F5m5My.png) ![Made Of Python](https://i.imgur.com/xNcFIbg.png)

### This is a Python program for dealing Mythic Cards in singleplayer, or local multiplayer

# Current Version
4.2.1

# Beta Version
5.0.0

# Support Always Appreciated
<a href="https://www.buymeacoffee.com/exarobibliologist" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# To Use
You will need Python installed on your computer.

[Python - Windows Store](https://apps.microsoft.com/detail/9nrwmjp3717k?hl=en-US&gl=US)

[Download from python.org](https://www.python.org/downloads/)

Open your Terminal after Python is installed and type

```
pip install pillow
```

You will need to have a downloaded copy of Mythic Cards RPG game. In the download, there is a folder filled with "Individual Card Images" in the .png format.

You won't need the Shuffle Card since this program automatically shuffles the cards on every deal, or the backs of the cards. Make a folder with just the card front images. As of v4, there is no need to pre-flip the images.

# Tutorial
![Picture of Program](https://i.imgur.com/FaYDpoF.png)

Run the Python program.

At the top of the window, there are three buttons (New, Save Load).

New will clear all of the text boxes, and reset the Chaos Factor slider for a new game.

Save will save all the information currently written in the program (Threads List, Chaos Factor, Characters List, and Storyline) to a save file that you can load later, or archive to show off your game. Multiple saves are possible, and you can save the file wherever you like.

Load can load those savefiles and restore an old game back to be played again.

The button Select Card Folder is used to load your digital deck of Mythic Cards. The program will display which folder is loaded, and how many .png images it located in the folder. This folder will be saved when you exit the program and will reload automatically the next time you open it.

Load Fate Chart will load the image titled FateChart.png which needs to be contained in the same folder as the Mythic RPG Card Dealer.py program.

You can use the Quickly Draw Cards buttons to quickly deal up to 10 cards. Alternatively, you can enter the number of cards you need dealt, and click the "Deal Cards" button below.

The Threads List is where you can write the list of threads your game has. Some of the cards will require you to build on one of those threads, and the "Select Random Threads List" will randomly pick one of your open threads and highlight it.

The Characters List functions like the Threads List, and its "Select Random Characters List" button will pick a random character and highlight it.

The Chaos Factor is a slider that goes from 1 to 9

In the Storyline box, you can write all the details of your emerging Mythic game storyline. Don't worry about filling any of the boxes with too much information; all the boxes can be scrolled with the mouse wheel.

# Known Bugs
None reported in v4.2.1

# Plans For The Future
* Support for laptops with low resolution screens.