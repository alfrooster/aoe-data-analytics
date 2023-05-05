#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

#replace with the location of your csv file
df = pd.read_csv("file-location")

##four lakes map win rates per civ in high elo

#filter to games in high elo (over 1300)
table_high = df.loc[df['rating.win'] >= 1300]
#filter to games in Four Lakes
fourlakes_table_high = table_high.loc[df['map_type.name']  == 'Four Lakes']

#wins with civ / all games with civ
fourlakes_winrates_high = fourlakes_table_high['civ.win.name'].value_counts()/(fourlakes_table_high['civ.win.name'].value_counts()+fourlakes_table_high['civ.lose.name'].value_counts())
#sort winrates and name columns
fourlakes_winrates_high = fourlakes_winrates_high.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})
#winrate to percentage
fourlakes_winrates_high.win_rate = fourlakes_winrates_high.win_rate * 100
#index starts from 1
fourlakes_winrates_high.index += 1

print(fourlakes_winrates_high)


# In[ ]:


##best civs in under 10 minute games
dura = df.loc[df['duration'] < '00:10:00']

civ_winrates_short = dura['civ.win.name'].value_counts()/(dura['civ.win.name'].value_counts()+dura['civ.lose.name'].value_counts())
civ_winrates_short = civ_winrates_short.sort_values(ascending = False).reset_index().rename(columns={'index':'civs',0:'win_rate'})
civ_winrates_short.win_rate = civ_winrates_short.win_rate * 100

print(civ_winrates_short)

