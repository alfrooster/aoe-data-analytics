import pandas as pd
import base64
from io import BytesIO
from matplotlib.figure import Figure

df = pd.read_csv("../aoe2.csv")

def formulate_strat(selected_map, selected_player_civ, selected_enemy_civ, selected_elo):

    #min and max for each selection
    if selected_elo == "all":
        elo_msg = "any"
    elif selected_elo == "low":
        elo_min, elo_max, elo_msg =     0,     1000,   "Low (under 1000)"
    elif selected_elo == "med":
        elo_min, elo_max, elo_msg =     1000,  1300,   "Mid (1000-1299)"
    elif selected_elo == "high":
        elo_min, elo_max, elo_msg =     1300,  10000,  "High (1300 or higher)"
    elif selected_elo == "veryhigh":
        elo_min, elo_max, elo_msg =     1500,  10000,  "Very High (1500 or higher)"

    #filter to games in chosen map
    table = df.loc[df['map_type.name']  == selected_map]

    #if user chooses all elo ranks, filtering by elo will be skipped
    if selected_elo != "all":
        #filter to games where elo is higher than user input
        table = table.loc[df['rating.win'] >= elo_min]
        #filter to games where elo is lower than user input
        table = table.loc[df['rating.win'] < elo_max]

    #filter to player civ as winner
    player_win_table = table.loc[df['civ.win.name'] == selected_player_civ]
    #filter to enemy civ as loser
    player_win_table = player_win_table.loc[df['civ.lose.name'] == selected_enemy_civ]
    
    #filter to enemy civ as winner
    enemy_win_table = table.loc[df['civ.win.name'] == selected_enemy_civ]
    #filter to player civ as loser
    enemy_win_table = enemy_win_table.loc[df['civ.lose.name'] == selected_player_civ]

    #calculate total games
    total_games = len(player_win_table) + len(enemy_win_table)

    #calculate win percentage
    if total_games == 0:
        win_percentage = "NO_DATA"
    else:
        win_percentage = len(player_win_table) / total_games * 100
        win_percentage = round(win_percentage, 2)

    return_object = {
        "total_games": total_games,
        "selected_player_civ": selected_player_civ,
        "win_percentage": win_percentage,
        "selected_enemy_civ": selected_enemy_civ,
        "selected_map": selected_map,
        "elo_msg": elo_msg
    }

    return return_object
    #return(f'According to our data of {total_games} games, the {selected_player_civ} have a {win_percentage}% chance of winning over the {selected_enemy_civ} in the map "{selected_map}" in {elo_msg} elo ranking.')

def analyze_winrates(selected_elo, selected_map, selected_duration):

    #filter to games where elo is higher than user input
    table_high = df.loc[df['rating.win'] >= int(selected_elo)]
    
    #filter to games in chosen map
    map_table_high = table_high.loc[df['map_type.name']  == selected_map]
    #filter by duration
    map_table_high = map_table_high.loc[map_table_high['duration'] < selected_duration]

    #wins with civ / all games with civ
    map_winrates_high = map_table_high['civ.win.name'].value_counts()/(map_table_high['civ.win.name'].value_counts()+map_table_high['civ.lose.name'].value_counts())
    #sort winrates and name columns
    map_winrates_high = map_winrates_high.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})
    #winrate to percentage
    map_winrates_high.win_rate = map_winrates_high.win_rate * 100
    #index starts from 1
    map_winrates_high.index += 1

    fig = Figure()
    ax = fig.subplots()
    ax.pie(map_winrates_high.win_rate.iloc[0:5], labels=map_winrates_high.civs.iloc[0:5], autopct='%.1f%%')
    fig.savefig('./static/images/plot.png')

    #print top 5 civs
    return map_winrates_high.head(5).to_html()