import numbers
import time
from functools import cmp_to_key

import requests
from pycqBot.cqApi import Message

mode_names = {
    3: "三人麻将",
    "3": "三人麻将",
    4: "四人麻将",
    "4": "四人麻将",
}

order = {
    0: "一位",
    1: "二位",
    2: "三位",
    3: "四位",
}

def search_basic_info(name, mode=3):
    session = requests.Session()
    url = f"https://3.data.amae-koromo.com/api/v2/pl{mode}/search_player/{name}?limit=5"
    response = session.get(url)
    content = response.json()
    assert(len(content) > 0)
    return content[0]

def search_detailed_info(id, mode="3", start=1262304000000, end=int(time.time()*1000)):
    session = requests.Session()
    mode = int(mode)
    headers = {'Cache-Control': 'no-cache'}
    if mode == 3:
        url = f"https://1.data.amae-koromo.com/api/v2/pl3/player_extended_stats/{id}/{start}/{end}?mode=21,22,23,24,25,26"
    else:
        url = f"https://1.data.amae-koromo.com/api/v2/pl4/player_extended_stats/{id}/{start}/{end}?mode=8,9,11,12,15,16"
    response = session.get(url, headers=headers)
    content = response.json()
    msgs = [f"以下仅统计{mode_names[mode]}金之间及以上比赛数据"]
    try:
        content.pop("count")
        content.pop("id")
        content.pop("played_modes")
        content.pop("最近大铳")
    except:
        pass
    for key, value in content.items():
        if key[-1] == "率" and key[-2] != "效":
            msgs.append(f"{key}: {'%.2f%%'%(value*100) if isinstance(value, numbers.Number) else '无数据'}")
        else:
            msgs.append(f"{key}: {'%.2f'%(value) if isinstance(value, float) else value}")
    return "\n".join(msgs)

def search_recent_info(id, mode="3", num=10, indetail=False, start=1262304000000, end=int(time.time()*1000)):
    session = requests.Session()
    id = int(id)
    mode = int(mode)
    headers = {'Cache-Control': 'no-cache'}
    if mode == 3:
        url = f"https://1.data.amae-koromo.com/api/v2/pl3/player_records/{id}/{end}/{start}?limit={num}&mode=21,22,23,24,25,26&descending=true"
    else:
        url = f"https://1.data.amae-koromo.com/api/v2/pl4/player_records/{id}/{end}/{start}?limit={num}&mode=8,9,11,12,15,16&descending=true"
    response = session.get(url, headers=headers)
    content = response.json()
    msgs = [f"以下倒序呈现{mode_names[mode]}金之间及以上最近{len(content)}场比赛数据"]
    for record in content:
        players = sorted(record["players"], key=cmp_to_key(lambda x, y: -x["score"] + y["score"]))
        record_time = time.strftime('%Y/%m/%d %H:%M', time.localtime(record["endTime"]))
        for i in range(len(players)):
            player = players[i]
            if player["accountId"] == id:
                if indetail:
                    msgs.append(f"{record_time}，{order[i]}，点数: {player['score']}，积分: {player['gradingScore']}，牌谱: {record['uuid']}")
                else:
                    msgs.append(f"{record_time}，{order[i]}，点数: {player['score']}，积分: {player['gradingScore']}")
    return "\n".join(msgs)

def info(commandData, message: Message):
    try:
        name = commandData[0]
        mode = commandData[1]
        assert mode in ["3", "4"]
    except:
        message.reply("查询命令有误！")
        return
    try:
        basic_info = search_basic_info(name, mode=mode)
        detailed_info = search_detailed_info(basic_info["id"], mode=mode)
        message.reply(detailed_info)
    except AssertionError:
        message.reply(f"未查到玩家{name}的相关信息，请确保其{mode_names[mode]}段位达到雀杰及以上！")
    except Exception as e:
        message.reply(f"服务器出错: {e}")

def recent(commandData, message: Message):
    try:
        name = commandData[0]
        mode = commandData[1]
        assert mode in ["3", "4"]
        try:
            num = int(commandData[2])
        except IndexError:
            num = 10
        try:
            indetail = commandData[3]
        except IndexError:
            indetail = "否"
        assert indetail in ["是", "否"]
        indetail = True if indetail == "是" else False
    except:
        message.reply("查询命令有误！")
        return
    try:
        basic_info = search_basic_info(name, mode=mode)
        recent_info = search_recent_info(basic_info["id"], mode=mode, num=num, indetail=indetail)
        message.reply(recent_info)
    except AssertionError:
        message.reply(f"未查到玩家{name}的相关信息，请确保其{mode_names[mode]}段位达到雀杰及以上！")
    except Exception as e:
        message.reply(f"服务器出错: {e}")