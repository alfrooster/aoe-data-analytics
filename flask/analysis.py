import pandas as pd

df = pd.read_csv("../aoe2.csv")

def formulate_strat(selected_map, selected_player_civ, selected_enemy_civ, selected_elo):

    #min and max for each selection
    if selected_elo == "all":
        elo_msg = "any"
    if selected_elo == "low":
        elo_min = 0
        elo_max = 1000
        elo_msg = "Low (<1000)"
    elif selected_elo == "med":
        elo_min = 1000
        elo_max = 1300
        elo_msg = "Medium (1000-1300)"
    elif selected_elo == "high":
        elo_min = 1300
        elo_max = 10000
        elo_msg = "High (over 1300)"
    elif selected_elo == "veryhigh":
        elo_min = 1500
        elo_max = 10000
        elo_msg = "Very High (over 1500)"

    #filter to games in chosen map
    table = df.loc[df['map_type.name']  == selected_map]

    if selected_elo != "all":
        #filter to games where elo is higher than user input
        table = table.loc[df['rating.win'] >= elo_min]
        #filter to games where elo is lower than user input
        table = table.loc[df['rating.win'] <= elo_max]

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

    if total_games == 0:
        win_percentage = "NO_DATA"
    else:
        #calculate win percentage
        win_percentage = len(player_win_table) / total_games * 100
        win_percentage = round(win_percentage, 2)

    return(f'According to our data of {total_games} games, {selected_player_civ} have a {win_percentage}% chance of winning over {selected_enemy_civ} in the map "{selected_map}" in {elo_msg} elo ranking.')

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

    #print top 5 civs
    return map_winrates_high.head(5).to_html()