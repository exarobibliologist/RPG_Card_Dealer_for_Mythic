# RPG_Card_Dealer_for_Mythic

![Made For Mythic Cards](https://i.imgur.com/1F5m5My.png) ![Made Of Python](https://i.imgur.com/xNcFIbg.png)

### This is a Python program for dealing Mythic Cards in singleplayer, or local multiplayer

# Current Version
5.3.156

[If it breaks, please tell me where so I can find both pieces.](https://github.com/exarobibliologist/RPG_Card_Dealer_for_Mythic/issues)

# Support Always Appreciated
<a href="https://www.buymeacoffee.com/exarobibliologist" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>

# To Use
You will need Python with Pip installed on your computer.

If you use Windows 11, it is easier to install Python from the Microsoft store.
[Python - Windows Store](https://apps.microsoft.com/detail/9nrwmjp3717k?hl=en-US&gl=US)

For other operating systems (Mac, Linux)
[Download from python.org](https://www.python.org/downloads/)

Open your Terminal after Python is installed and type

```
pip install pillow
```

You will need to have a downloaded copy of Mythic Cards RPG game. In the download, there is a folder filled with "Individual Card Images" in the .png format.

You won't need the Shuffle Card, since this program automatically shuffles the cards on every deal. You also will not need the backs of the cards. Select the card fronts, and copy them to a new folder.

As of v4+, there is no need to flip the cards yourself anymore. The program should flip the cards randomly during the draw.

As of v5+, app displays in two windows, suitable for small resolution laptop screens.

# Tutorial
![Picture of Program](https://i.imgur.com/PQTQvpg.png)

Run the Python program. You will see two windows.

### Window 1 - Mythic RPG Card Dealer

"Select Card Folder" allows you to choose the folder where you have saved your deck of Mythic Cards. The program will display which folder is loaded, and how many card images it located in the folder. This folder will be saved when you exit the program and will reload automatically the next time you open it.

You can click "Show Fate Chart" to load the image titled FateChart.png which needs to be contained in the same folder as the Mythic RPG Card Dealer.py program.

The Quickly Draw Cards row of buttons allows you to quickly deal up any number of cards up to 10.

If you need to deal more than 10, type the number in the box below and click "Deal Cards".

### Window 2 - Mythic Game Notes

**NOTE: This window is a child window of the main window. The X displays in the corner but does nothing. You can only close the program by closing the main window.** ***Make sure to save your work before you do that!***

At the top of the window, click "New" to begin a new game; click "Save" to save a current game; click "Load" to load your last saved game. The Save button at the top of the window will save all the information currently written in the program (Threads List, Chaos Factor, Characters List, and Storyline) to a text file formatted to be read by the program. You can save this file wherever you want, and reload it at a later time.

When you reopen the program, it will start out blank, but you can click Load to reload your save file and continue your game. Multiple saves are allowed. Go have fun!

The Threads List is where you can write the list of threads your game has. Some of the cards will require you to build on one of those threads, and the "Select Random Threads List" will randomly pick one of your open threads and highlight it.

The Characters List functions like the Threads List, and its "Select Random Characters List" button will pick a random character and highlight it.

The Chaos Factor is a slider that goes from 1 to 9

In the Storyline box, you can write all the details of your emerging Mythic game storyline. Don't worry about filling any of the boxes with too much information; all the boxes can be scrolled with the mouse wheel.

# Plans for the Future
1. **Autosave** - This tanked out epically in recent design and development, but I may attempt to add this function at a later date.
2. **Support for regular Mythic games** - Mythic and Mythic Cards have similar rules, but vary in enough places that I may end up having to design a different app for normal Mythic games, but I plan to look into this in the future.