import logging

from pycqBot.cqApi import Message, cqHttpApi, cqLog

from instr.divine import divine
# 启用日志 默认日志等级 DEBUG
cqLog(logging.INFO)

cqapi = cqHttpApi()

# echo 函数
def echo(commandData, message: Message):
    # 回复消息
    message.reply(" ".join(commandData))

bot = cqapi.create_bot(
    group_id_list=[
        # 需处理的 QQ 群信息 为空处理所有
        476931131,
        421721306
    ],
)

# 设置指令为 echo
bot.command(echo, "echo", {
    # echo 帮助
    "help": [
        "#echo - 输出文本"
    ]
}).command(divine, "抽签", {
    "help": [
        "#抽签 - 抽取运势"
    ]
}).start()
