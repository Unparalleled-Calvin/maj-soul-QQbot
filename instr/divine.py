import json
import random
import logging
from pathlib import Path

from pycqBot.cqApi import Message

def load_sticks(FILE_NAME="sticks.json", DIR_NAME="asset"):
    file_path = Path(DIR_NAME, FILE_NAME)

    if not file_path.exists():
        logging.error(f"File Not Found! Visit https://github.com/Tamshen/senso-ji-stick-data/blob/master/data.zh.json to download data into {str(file_path)}")
        quit()

    with file_path.open(mode="r", encoding="utf-8") as f:
        all_sticks = json.load(f)["qcs"]
    
    return all_sticks

def parctice_divination(QID, FILE_NAME="record.json", DIR_NAME="data\\divinations"):
    file_path = Path(DIR_NAME, FILE_NAME)
    msg = ""
    QID = str(QID)
    try:
        with file_path.open(mode="r") as f:
            record = json.load(f)
    except:
        record = {}
    if QID not in record:
        index = random.randint(1, len(all_sticks) - 1)
        record[QID] = index
        with file_path.open(mode="w") as f:
            json.dump(record, f)
    else:
        index = record[QID]
        msg += "您今天已经抽过签了！\n"
    msg += "\n".join(all_sticks[0] + all_sticks[index])
    return msg

def divine(commandData, message: Message):
    divination = parctice_divination(message.user_id)
    message.reply(divination)


all_sticks = load_sticks()