from pycqBot.cqApi import Message

import requests
import time
import numbers

mode_names = {
    3: "三人麻将",
    "3": "三人麻将",
    4: "四人麻将",
    "4": "四人麻将",
}

def search_basic_info(name, mode=3):
    session = requests.Session()
    url = f"https://3.data.amae-koromo.com/api/v2/pl{mode}/search_player/{name}?limit=5"
    response = session.get(url)
    content = response.json()
    if len(content) < 1:
        return {}
    else:
        return content[0]

def search_detailed_info(id, mode="3", start=1262304000000, end=int(time.time())):
    session = requests.Session()
    mode = int(mode)
    if mode == 3:
        url = f"https://3.data.amae-koromo.com/api/v2/pl3/player_extended_stats/{id}/{start}/{end}?mode=22"
    else:
        url = f"https://1.data.amae-koromo.com/api/v2/pl4/player_extended_stats/{id}/{start}/{end}?mode=9"
    response = session.get(url)
    content = response.json()
    msgs = [f"以下仅统计{mode_names[mode]}金之间及以上比赛数据"]
    try:
        msgs.append(f"总局数: {content.pop('count')}")
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
    except KeyError:
        message.reply(f"未查到玩家{name}的相关信息，请确保其{mode_names[mode]}段位达到雀杰及以上！")
    except:
        message.reply("服务器出错！")