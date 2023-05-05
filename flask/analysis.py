import pandas as pd
import base64
from io import BytesIO
# from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from matplotlib.figure import Figure

df = pd.read_csv("./aoe2.csv")

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
        pie_data = [50, 50]
    else:
        win_percentage = len(player_win_table) / total_games * 100
        win_percentage = round(win_percentage, 2)
        pie_data = [win_percentage, 100 - win_percentage]

    civs = [selected_player_civ, selected_enemy_civ]

    fig = Figure()
    ax = fig.subplots()
    ax.pie(pie_data, labels=civs, autopct='%.1f%%')
    fig.savefig('./flask/static/images/plot.png')

    return_object = {
        "total_games": total_games,
        "selected_player_civ": selected_player_civ,
        "win_percentage": win_percentage,
        "selected_enemy_civ": selected_enemy_civ,
        "selected_map": selected_map,
        "elo_msg": elo_msg
    }

    return return_object

def analyze_winrates(selected_elo, selected_map, selected_fromduration, selected_toduration):

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

    if int(selected_fromduration) <= 0:
        min_dura = "00:00:00"
    elif int(selected_fromduration) <= 5 and int(selected_fromduration) > 0:
        min_dura = "00:05:00"
    elif int(selected_fromduration) >= 10:
        min_dura = f"00:{selected_fromduration}:00"
    if int(selected_toduration) <= 60 and int(selected_toduration) >= 0:
        max_dura = f"00:{selected_toduration}:00"
    elif int(selected_toduration) > 60:
        max_dura = "99:99:99"

    #filter to games in chosen map
    table = df.loc[df['map_type.name']  == selected_map]

    #if user chooses all elo ranks, filtering by elo will be skipped
    if selected_elo != "all":
        #filter to games where elo is higher than user input
        table = table.loc[df['rating.win'] >= elo_min]
        #filter to games where elo is lower than user input
        table = table.loc[df['rating.win'] < elo_max]

    #filter by duration
    table = table.loc[table['duration'] >= min_dura]
    table = table.loc[table['duration'] < max_dura]

    #calculate total games
    total_games = len(table)

    #wins with civ / all games with civ
    winrate_table = table['civ.win.name'].value_counts()/(table['civ.win.name'].value_counts()+table['civ.lose.name'].value_counts())
    #sort winrates and name columns
    winrate_table = winrate_table.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})

    #winrate to percentage
    winrate_table.win_rate = round(winrate_table.win_rate * 100, 2)
    #index starts from 1
    winrate_table.index += 1

    fig = plt.figure(figsize= (10, 7))
    ax = fig.subplots()
    plt.bar(winrate_table.civs.iloc[0:5], winrate_table.win_rate.iloc[0:5])
    ax.set(ylim=[49, 100])
    fig.savefig('./flask/static/images/plot.png')

    winrate_table.columns = winrate_table.columns.str.replace('civs', "Civilizations")
    winrate_table.columns = winrate_table.columns.str.replace('win_rate', "Win Percentage")

    return_object = {
        "table": winrate_table.head(5).to_html(), #top 5 civs
        "total_games": total_games,
        "selected_map": selected_map,
        "min_dura": min_dura,
        "max_dura": max_dura,
        "elo_msg": elo_msg
    }

    return return_object