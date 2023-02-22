import re
from pathlib import Path

from PIL import Image
from pycqBot.cqApi import Message
from pycqBot.cqCode import image

TILE_WIDTH = 80
TILE_HEIGHT= 129
GAP = 1

def get_all_tiles(FILE_NAME="myres.png", DIR_NAME="asset"):
    im = Image.open(Path(DIR_NAME, FILE_NAME))
    names = [
        "7s", "7w", "9p", "1s", "3s",
        "5p", "7p", "9s", "1z", "2z",
        "5s", "0p", "b", "2w", "4w",
        "5z", "7z", "4z", "2p", "4p",
        "6w", "8w", "0w", "2s", "4s",
        "6p", "8p", "0s", "3z", "5w",
        "6s", "8s", "1w", "3w", "-1",
        "6z", "9w", "1p", "3p", "-1"
    ]
    tiles = []
    for left in range(0, 647, TILE_WIDTH + GAP):
        right = left + TILE_WIDTH
        for upper in range(0, 649, TILE_HEIGHT + GAP):
            lower = upper + TILE_HEIGHT
            tiles.append(im.crop((left, upper, right, lower)))
    return dict(zip(names, tiles))

def parse(curse): #格式为[\b+]{pwsz}
    pattern = re.compile(r"(\d+[pwsz]|b)")
    parts = re.findall(pattern, curse)
    if "".join(parts) != curse:
        return "格式错误", None
    names = []
    for part in parts:
        if part[-1] == "b":
            names.append("b")
        for c in part[:-1]:
            if part[-1] == "z" and (c == "0" or c >= "8"):
                return f"格式错误：无{c}z", None
            names.append(c + part[-1])
    return "", names

def gen_tiles_pic(tiles, names):
    num = len(names)
    joint = Image.new('RGBA', (num * TILE_WIDTH, TILE_HEIGHT))
    for i in range(num):
        name = names[i]
        joint.paste(tiles[name], (TILE_WIDTH * i, 0))
    return joint

tiles = get_all_tiles()

def render(commandData, message: Message):
    curse = commandData[0]
    err, names = parse(curse)
    if names is None:
        message.reply(err)
    else:
        pic = gen_tiles_pic(tiles, names)
        pic.save("data/images/temp_tiles.png")
        message.reply("%s" % image("temp_tiles.png"))
