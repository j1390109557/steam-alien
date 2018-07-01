import requests
import json
import time
plant_list = []
access_token = 'fe8ff1a4aa28101fbd1908e2ab9a5c38'
room_id = 0
count = 1
plant_id =508
difficultys_list = ['低','中','高']
def play_game():
        play_games = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlayerInfo/v0001/',data = {'access_token':access_token})
        levels = play_games.json()["response"]["level"]
        scores = play_games.json()["response"]["score"]
        next_level_scores = play_games.json()["response"]["next_level_score"]
        print('当前等级: '+ str(levels),'当前分数: ' + str(scores) + "/" + next_level_scores)
def get_plant():
        select_plant = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/JoinPlanet/v0001/',data = {'id':plant_id,'access_token':access_token})
        plant = requests.get('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlanet/v0001/?id='+str(plant_id)+'&language=schinese',data = {'id':plant_id,'language':'schinese'})
        plants = plant.json()["response"]["planets"][0]
        name = plants['state']['name']
        print('当前星球 : ' + name)
def go_room():
        global room_id
        goto_room = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/JoinZone/v0001/',data = {'zone_position':room_id,'access_token':access_token})
        room = goto_room.json()['response']
        #print(room)
        if room !={}:
                zone_position = room['zone_info']['zone_position']
                difficulty = room['zone_info']['difficulty']
                print('进入房间成功,等待110s发送分数,房间ID: {} , 难度等级: {}'.format(zone_position,difficultys_list[difficulty - 1]))
                if difficulty == 3:
                        score = 2400
                        send_score(score)
                elif difficulty == 2:
                        score = 1200
                        send_score(score)
                        room_id = room_id + 1
                else:
                        score = 600
                        send_score(score)
                        room_id = room_id + 1

        else:
                print('进入房间失败')
                select_room()



def send_score(score):
        time.sleep(110)
        get_score = requests.post('https://community.steam-api.com/ITerritoryControlMinigameService/ReportScore/v0001/',data = {'access_token':access_token,'score':score,'language':'schinese'})
        score = get_score.json()["response"]
        try:
                #分数
                new_score = score['new_score']
                #等级
                new_level = score["new_level"]
                #下一级需要分数
                next_score = score["next_level_score"]
                print('新等级 {} ，当前经验值 {} ,升到 {} 级需要经验 {} ,还差 {} 经验'.format(new_level,new_score,str(int(new_level)+int(1)),next_score,int(next_score) - int(new_score)))
        except KeyError:
                print('分数发送失败，可能是由于您登陆了网页版，正在重试')
                get_plant()
                go_room()
                send_score(score)
def select_room():
        global room_id
        global count
        global plant_id
        room_id = room_id + 1
        if room_id == 97:
                print('本星球没有可以战斗的房间，正在切换星球')
                room_id = 0
                plant_list.clear()
                select_plant()
                try:
                        plant_id = plant_list[count]
                        get_plant()
                        count = count + 1
                except IndexError:
                        print('没有可以切换的星球了,正在重置')
                        count = 0
                        room_id = 0
                        get_plant()



def select_plant():
    get_plant = requests.get('https://community.steam-api.com/ITerritoryControlMinigameService/GetPlanets/v0001/?active_only=0&language=schinese')
    for i in range(52):
        select_plant = get_plant.json()["response"]["planets"][i]
        select_captured= select_plant['state']['captured']
        select_active = select_plant['state']['active']

        if select_active and not select_captured:
            plant_list.append(select_plant['id'])

play_game()
get_plant()
while True:
        go_room()
