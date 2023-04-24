import pandas as pd

df = pd.read_csv("C:/Users/alfre/aoe-data-analytics/aoe2.csv")

def formulate_strat(selected_map, selected_player_civ, selected_enemy_civ, selected_elo):

    #min and max for each selection
    if selected_elo == "all":
        elo_msg = "any"
    elif selected_elo == "low":
        elo_min = 0
        elo_max = 1000
        elo_msg = "Low (under 1000)"
    elif selected_elo == "med":
        elo_min = 1000
        elo_max = 1300
        elo_msg = "Mid (1000-1299)"
    elif selected_elo == "high":
        elo_min = 1300
        elo_max = 10000
        elo_msg = "High (1300 or higher)"
    elif selected_elo == "veryhigh":
        elo_min = 1500
        elo_max = 10000
        elo_msg = "Very High (1500 or higher)"

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

    return(f'According to our data of {total_games} games, the {selected_player_civ} have a {win_percentage}% chance of winning over the {selected_enemy_civ} in the map "{selected_map}" in {elo_msg} elo ranking.\
           \r\nWinning chance: {win_percentage}%\nPlayer civilization: {selected_player_civ}\nOpponent civilization: {selected_enemy_civ}\nMap: {selected_map}\nRanking: {selected_elo}')

def analyze_winrates(selected_elo, selected_map, selected_duration):

    #min and max for each selection
    if selected_elo == "all":
        elo_msg = "any"
    elif selected_elo == "low":
        elo_min = 0
        elo_max = 1000
        elo_msg = "Low (under 1000)"
    elif selected_elo == "med":
        elo_min = 1000
        elo_max = 1300
        elo_msg = "Mid (1000-1299)"
    elif selected_elo == "high":
        elo_min = 1300
        elo_max = 10000
        elo_msg = "High (1300 or higher)"
    elif selected_elo == "veryhigh":
        elo_min = 1500
        elo_max = 10000
        elo_msg = "Very High (1500 or higher)"

    #filter to games in chosen map
    table = df.loc[df['map_type.name']  == selected_map]

    #if user chooses all elo ranks, filtering by elo will be skipped
    if selected_elo != "all":
        #filter to games where elo is higher than user input
        table = table.loc[df['rating.win'] >= elo_min]
        #filter to games where elo is lower than user input
        table = table.loc[df['rating.win'] < elo_max]

    #filter by duration
    table = table.loc[table['duration'] < selected_duration]

    #wins with civ / all games with civ
    winrate_table = table['civ.win.name'].value_counts()/(table['civ.win.name'].value_counts()+table['civ.lose.name'].value_counts())
    #sort winrates and name columns
    winrate_table = winrate_table.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})
    #winrate to percentage
    winrate_table.win_rate = winrate_table.win_rate * 100
    #index starts from 1
    winrate_table.index += 1

    ##winrate_table.style.set_caption(f'Top civilizations in "{selected_map} in {selected_elo} ranking')

    #print top 5 civs
    return winrate_table.head(5).to_html()