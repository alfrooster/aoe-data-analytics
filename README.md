# Age of Empires 2 - Data-analysis

The goals of this project is to analyze the ranked multiplayer match data of the video game Age of Empires 2, and see if there are reasonable conclusions to be made on which variables affect the chances of victory.
These variables consist of match settings, such as map type, player-picked civilization, and other possible determining factors.

The analysis was done utilizing Python's [pandas](https://pandas.pydata.org/)-library. We also used [matplotlib](https://matplotlib.org/) to draw charts in the results.

The data we used is from: https://www.kaggle.com/datasets/slappdun/35000-age-of-empires-2-1v1-ranked-random-matches

## Usage
The player goes into a match. They choose the map. They match up with another player and they get random civilizations. The player can then use our app to see their chance of winning. From our app they choose the map, their civilization, their opponents civilization and their skill level, the elo rank. The app then gives them the chance of winning as a percentage based on our data.

Our app can also be used to see a list of the best civilizations in a specific map. You can also specify the search by choosing the skill level (elo) and the match duration in case you would like to see if different civilizations have different win percentages in longer or shorter matches.

## Installation
1. Clone the repository
2. Install virtual environment `pip3 install virtualenv`
3. Setup virtual environment `python -m venv venv`
4. Activate virtual environment `venv\Scripts\activate`
5. Install requirements `pip install -r requirements.txt`
6. Launch app `python app.py`
