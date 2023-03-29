import pandas as pd

def analyse():

    df = pd.read_csv("./aoe2.csv")

    # WILL BE REPLACED BY USER INPUT
    #ask user for elo
    elo = 200 #int(input("Minimum elo: "))
    #ask user for map (case sensitive)
    map = "Arabia" #input("Map: ")
    #ask user for maximum duration
    dura = "00:30:00" #input("Match duration max (HH:MM:SS): ")

    #filter to games where elo is higher than user input
    table_high = df.loc[df['rating.win'] >= elo]
    listmaps = []
    for i in df['map_type.name']:
        if i not in listmaps:
            listmaps.append(i)
    #print(sorted(listmaps))
    
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
    return map_winrates_high.head(5).to_html()