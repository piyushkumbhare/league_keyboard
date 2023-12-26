import requests
import json
import urllib3
import time

import champ_animations


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)#guh, I dont wanna see these warnings anymore :]



api_key = "RGAPI-9531a98b-420e-41ad-b738-d273447831f7" #update daily, may be needed for future add-ons, found at https://developer.riotgames.com

#update these two to your own if you want to run non-local PUUID paths
name = 'zSuper'
tagline = 'SKZ'

account_url = "https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/" + name + '/' + tagline + '/'
mastery_url = "https://na1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/" #for testing PUUID
ingame_url = "https://127.0.0.1:2999/liveclientdata/allgamedata" #For getting live game client data
dd_version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
version_num = requests.get(dd_version_url).json()[0] #current version of the game from DataDragon
dd_champ_url = f"https://ddragon.leagueoflegends.com/cdn/{version_num}/data/en_US/champion" #all champion data from DataDragon

lockfile_path = "C:\Riot Games\League of Legends\lockfile" #CHANGE TO LOCKFILE LOCATION, usually in Riot Games\League of Legends

port = ''
pwd = ''
id = 0
champ_name = ''

with open(lockfile_path, 'r') as file: #gets password and port num from lockfile
    line = file.read()
    components = line.rsplit(':')
    print(components)
    port = components[2]
    pwd = components[3]

while True: #Pings every second in champ select, breaks once player selects champ: 
    time.sleep(1)
    try:
        selected_champ = requests.get(f'https://riot:{pwd}@127.0.0.1:{port}/lol-champ-select/v1/current-champion', verify=False)
        selected_champ.raise_for_status()
        if selected_champ.json() == 0:
            print(0) #0 if no champ is selected
        else:
            print(selected_champ.json())
            id = selected_champ.json() #champ id when champ is selected
            break
    except Exception as e: #ignore if not in champ select yet
        print(-1)


champ_data = requests.get(dd_champ_url + '.json') #GET from DataDragon to match id to champion name
champions = champ_data.json()['data']
for champ in champions.keys():
    if champions[champ]['key'] == str(id):
        champ_name = champions[champ]['id']


print(champ_name)

# def combiner(url):
#     return url + '?api_key=' + api_key

def champFinder(champName): #find champ details from dataDragon
    return dd_champ_url + '/' + champName + '.json'

# data = requests.get(combiner(account_url))
# print(data.json())
# puuid = data.json()['puuid']
# print(puuid)

# ingame_data = requests.get(ingame_url, verify=False)
# print(ingame_data.json())

Q_cd, Q_cost, W_cd, W_cost, E_cd, E_cost, R_cd, R_cost = None, None, None, None, None, None, None, None

data = requests.get(dd_champ_url + '/' + champ_name + '.json') #gets list of spell costs and cooldowns from DataDragon, per level
count = 0
for spell in data.json()['data'][champ_name]['spells']:
    if count == 0:
        Q_cost = spell['cost']
        Q_cd = spell['cooldown']
    if count == 1:
        W_cost = spell['cost']
        W_cd = spell['cooldown']
    if count == 2:
        E_cost = spell['cost']
        E_cd = spell['cooldown']
    if count == 3:
        R_cost = spell['cost']
        R_cd = spell['cooldown']
    count+=1

print('cooldown of Q per level is: ' + str(Q_cd))
print('cooldown of W per level is: ' + str(W_cd))
print('cooldown of E per level is: ' + str(E_cd))
print('cooldown of R per level is: ' + str(R_cd))
