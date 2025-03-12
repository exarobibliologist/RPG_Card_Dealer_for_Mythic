# RPG_Card_Dealer_for_Mythic

![Made For Mythic Cards](https://i.imgur.com/1F5m5My.png) ![Made Of Python](https://i.imgur.com/xNcFIbg.png)

### This is a Python program for dealing Mythic Cards in singleplayer, or local multiplayer

# Current Version
[3.0.0](https://github.com/exarobibliologist/RPG_Card_Dealer_for_Mythic/releases/tag/v3.0.0)

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

You won't need the Shuffle Card, since this program automatically shuffles the cards on every deal. You also will not need the backs of the cards. Select the card fronts, and copy them to a new folder. Use your preferred image editor to flip the cards 180°, save them with a different file name so they don't overwrite the original files, then put them back in the original folder.

All of the cards (original and flipped) must be in the same folder.

# Tutorial
![Picture of Program](https://i.imgur.com/Ihv1jIq.png)

Run the Python program. At the top of the window, there is a button to Load Cards. Select the folder where you have your digital card deck located. The program will display which folder is loaded, and how many .png images it located in the folder. This folder will be saved when you exit the program and will reload automatically the next time you open it.

You can click "Load Fate Chart" to load the image titled FateChart.png which needs to be contained in the same folder as the Mythic RPG Card Dealer.py program.

You can use the Quick Deal buttons to quickly deal up to 10 cards. Alternatively, you can enter the number of cards you need dealt, and click the "Deal Cards" button below.

The Threads List is where you can write the list of threads your game has. Some of the cards will require you to build on one of those threads, and the "Select Random Threads List" will randomly pick one of your open threads and highlight it.

The Characters List functions like the Threads List, and its "Select Random Characters List" button will pick a random character and highlight it.

The Chaos Factor is a slider that goes from 1 to 9

In the Storyline box, you can write all the details of your emerging Mythic game storyline. Don't worry about filling any of the boxes with too much information; all the boxes can be scrolled with the mouse wheel.

The Save button at the top of the window will save all the information currently written in the program (Threads List, Chaos Factor, Characters List, and Storyline) to a "saved_data.txt" file in the directory where you have the Mythic RPG Card Dealer.py program stored.

When you reopen the program, it will start out blank, but you can click Load to reload your save file and continue your game. You can only have one save file in the program directory at a time. Multiple saves not supported yet.

Here's an example of the program in use from a recent game I played.

![](https://i.imgur.com/wqG6x9Y.png)

# Known Bugs
None in v3.0.0
1 reported bug in v4.0.0-beta [Please report any bugs here](https://github.com/exarobibliologist/RPG_Card_Dealer_for_Mythic/issues)

# Plans For The Future
* Make the app flip the cards itself during the display process. *(Currently in BETA) (Release Date: SOON!)*
* Allow multiple save files to be created. Redesign Load to allow you choose a file to be loaded.
