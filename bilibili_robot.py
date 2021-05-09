from datetime import datetime as date
from os import linesep
from time import sleep

from services.bilibili_client import BilibiliClient
from services.config import Config
from services.email_client import EmailClient


def add_content(line):
    global content
    content = content.__add__(line).__add__(linesep)



# 当前日期
config = Config()
config.print()
email = EmailClient(config)
date_str = date.now().strftime('%Y-%m-%d')
print(date_str)
subject = f"哔哩哔哩机器人🤖 {date_str} 执行报告"
content = ""

bilibili = BilibiliClient(config)
coin_before = bilibili.getCoin()
add_content(f"投币前硬币数量：{coin_before}!!!")

# rid=20 宅舞分区，猛男必看
# 其他分区 https://www.bookstack.cn/read/BilibiliAPIDocs/CONST.typeid.md
avs = bilibili.getRegions(rid=22, num=1)
add_content(f"获取到视频，开始投币")
for av in avs:
    bilibili.coin(av['aid'], 1, 1)
    add_content(f"为 https://www.bilibili.com/video/{av['bvid']} 投币完成")

sleep(10)
coin_after = bilibili.getCoin()
add_content(f"投币完成，硬币数量 {coin_after}!!!")
print(content)
email.send(subject, content)
print('执行完成')

