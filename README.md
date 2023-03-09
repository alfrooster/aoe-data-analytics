# aoe-data-analytics

The goals of this project is to analyze the ranked multiplayer match data of the video game Age of Empires 2, and see if there are reasonable conclusions to be made on which variables affect the chances of victory.
These variables consist of match settings, such as map type, player-picked civilization, and other possible determining factors.

The analysis is to be done utilizing Python's Pandas-library.

Some notes to help team: (subject to change)
1. Specifying the encoding for opening the .CSV-file: df = pd.read_csv(file, encoding='ISO-8859-1')
2. Install matplotlib (https://matplotlib.org/stable/users/installing/index.html) to use piecharts and other graphical visualisations
