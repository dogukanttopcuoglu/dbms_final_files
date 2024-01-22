import columns as columns
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def load():
    data = pd.read_csv("datasets/csgo_players_data.csv")
    return data

def load2():
    data = pd.read_csv("datasets/stats_value.csv")
    return data





df = load()
df.head()

'''Percentage verilerinden yüzde işareti kaldırma'''

# Yüzde işaretlerini kaldır

def removePercentage(dataframe, column_name):
    dataframe[column_name] = dataframe[column_name].str.rstrip('%').astype('float')
    return dataframe

removePercentage()

df_stats = load2()
df_stats.head()
removePercentage(df_stats, 'stats_value')
df_stats.to_csv('datasets\stats_id_value.csv', index=False)



removePercentage(df,'headshot_percentage')
removePercentage(df,'team_win_percent_after_first_kill')
removePercentage(df,'first_kill_in_won_rounds')




#check
df[['headshot_percentage','team_win_percent_after_first_kill','first_kill_in_won_rounds']]


df.to_csv('datasets\output.csv', index=False)















# 'teams' sütunundaki değerleri virgülle ayırdık     [Vitality,  aAa] gibi
df['teams'] = df['teams'].apply(lambda teams: teams.split(','))

df[['teams', 'current_team']]

#current_team de olup teams de olmayanları da oraya ekledik.(nan varsa eklememesine dikkat ettik.)
def merge_teams(row):
    if pd.notna(row['current_team']) and row['current_team'] not in row['teams']:
        row['teams'].append(row['current_team'])
    elif pd.isna(row['current_team']):
        row['teams'].append('000nan')
    return row['teams']

df['teams'] = df.apply(merge_teams, axis=1)

all_teams = [team for sublist in df['teams'] for team in sublist]
all_teams = [team.strip() if isinstance(team, str) else team for sublist in df['teams'] for team in sublist]


all_teams = set(all_teams)
num_unique_teams = len(all_teams)   #516 team

#önce sayıyla başlayan takımlar, sonra büyük harfle sonra da küçük harfle başlayanlar (all_teams sort ladık)
all_teams = sorted(list(all_teams), key=lambda x: (x.isdigit(), not x[0].isdigit(), x))

'''
#1337 ve 777 kod doğru olmasına rağmen en sona atıldı onları düzelttik.
all_teams.insert(5, 1337)
all_teams.pop(516)   #1337'i çıkartıp 4.indexe koydum

all_teams.insert(13, 777)
all_teams.pop(517) #777'yi çıkartıp 12.indexe koyduk
'''

# all_teams listesinden takım adlarına karşılık gelen ID'leri alın
team_id_mapping = dict(zip(all_teams, range(1, len(all_teams) + 1)))


'''team ve ona karşılık gelen team_id lerin csv'si hazırlandı.'''
team_id_df = pd.DataFrame(list(team_id_mapping.items()), columns=['team', 'team_id'])
team_id_df.to_csv('datasets\ team_id_table.csv', index=False)


'''player_id, teams ve is_current_team '''
df[['player_id', 'teams']]

#bazı takımların önünde fazladan boşluk vardı, kaldırdım.
df['teams'] = df['teams'].apply(lambda teams: [team.strip() for team in teams])

expanded_df = df.explode('teams')
expanded_df['is_current_team'] = (expanded_df['teams'] == expanded_df['current_team']).astype(int)



#player_id nin teamlerine karşılık gelen is_current_team lerin hepsi 0sa demekki current_team nan demektir.
expanded_df['team_id'] = expanded_df['teams'].map(team_id_mapping)

#expanded_df['team_id'] = expanded_df['team_id'].astype(int)



# Sonuçları gösterme
expanded_df[['player_id', 'teams', 'is_current_team', 'team_id']]
expanded_df.to_csv('datasets/ player_id_teams__id_is_current.csv', index=False)

# Sonuçları gösterme
expanded_df[['player_id', 'teams', 'is_current_team']]
expanded_df = expanded_df.drop_duplicates(subset=['player_id', 'teams', 'is_current_team'], keep='first')

nan_check = expanded_df['team_id'].isnull().any()
nan_rows = expanded_df[expanded_df['team_id'].isnull()]

nan_rows[['teams','team_id','is_current_team']]

last_df = expanded_df[['player_id', 'team_id', 'is_current_team']]

last_df.to_csv('datasets/ team_info_table.csv', index=False)

























