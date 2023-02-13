import logging

from pycqBot.cqApi import cqHttpApi, cqLog

from instr.divine import divine
from instr.info import info

# 启用日志 默认日志等级 INFO
cqLog(logging.INFO)

cqapi = cqHttpApi()


bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        476931131,
        421721306
    ],
)

# 设置指令为 echo
bot.command(divine, "抽签", {
    "help": [
        "#抽签 - 抽取运势"
    ]
}).command(info, "查询", {
    "help": [
        "#查询 用户名 模式 - 查询基本信息"
    ]
}).start()
