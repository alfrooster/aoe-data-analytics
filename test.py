import pandas as pd

#replace with the location of your csv file
df = pd.read_csv("aoe2.csv")

#ask user for elo
elo = int(input("Minimum elo: "))
#ask user for elo (case sensitive)
map = input("Map: ")

#filter to games where elo is higher than user input
table_high = df.loc[df['rating.win'] >= elo]
#filter to games in chosen map
fourlakes_table_high = table_high.loc[df['map_type.name']  == map]

#wins with civ / all games with civ
fourlakes_winrates_high = fourlakes_table_high['civ.win.name'].value_counts()/(fourlakes_table_high['civ.win.name'].value_counts()+fourlakes_table_high['civ.lose.name'].value_counts())
#sort winrates and name columns
fourlakes_winrates_high = fourlakes_winrates_high.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})
#winrate to percentage
fourlakes_winrates_high.win_rate = fourlakes_winrates_high.win_rate * 100
#index starts from 1
fourlakes_winrates_high.index += 1

#print top 5 civs
print(fourlakes_winrates_high.head(5))