import pandas as pd

#replace with the location of your csv file
df = pd.read_csv("C:/Users/alfre/Documents/archive/aoe2.csv")

#ask user for elo
elo = int(input("Minimum elo: "))
#ask user for map (case sensitive)
map = input("Map: ")
#ask user for maximum duration
dura = input("Match duration max (HH:MM:SS): ")

#filter to games where elo is higher than user input
table_high = df.loc[df['rating.win'] >= elo]
#filter to games in chosen map
map_table_high = table_high.loc[df['map_type.name']  == map]
#filter by duration
map_table_high = map_table_high.loc[map_table_high['duration'] < dura]

#wins with civ / all games with civ
map_winrates_high = map_table_high['civ.win.name'].value_counts()/(map_table_high['civ.win.name'].value_counts()+map_table_high['civ.lose.name'].value_counts())
#sort winrates and name columns
map_winrates_high = map_winrates_high.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})
#winrate to percentage
map_winrates_high.win_rate = map_winrates_high.win_rate * 100
#index starts from 1
map_winrates_high.index += 1

#print top 5 civs
print(map_winrates_high.head(5))