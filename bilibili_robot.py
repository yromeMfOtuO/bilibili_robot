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
reward_before = bilibili.get_reward()
add_content(f"当前等级：{reward_before['level_info']['current_level']}，当前经验：{reward_before['level_info']['current_exp']}")
coin_before = bilibili.get_coin()
add_content(f"投币前硬币数量：{coin_before}!!!")

# rid=20 宅舞分区，猛男必看
# 其他分区 https://www.bookstack.cn/read/BilibiliAPIDocs/CONST.typeid.md
avs = bilibili.get_regions(rid=20, num=5)
add_content(f"获取到视频，开始投币")
for av in avs:
    bilibili.add_coin(av['aid'], 2, 1)
    add_content(f"为 https://www.bilibili.com/video/{av['bvid']} 投币完成")

sleep(10)
coin_after = bilibili.get_coin()
add_content(f"投币完成，硬币数量 {coin_after}!!!")
print(content)

# 模拟观看视频
add_content("")
add_content("开始模拟观看视频")
report = bilibili.report(avs[0]['aid'], avs[0]['cid'], 300)
add_content(f"模拟观看视频 https://www.bilibili.com/video/{avs[0]['bvid']} 完成!!!")

# 分享视频
add_content("")
add_content("开始分享视频")
share = bilibili.share(avs[0]['aid'])
add_content(f"分享视频 https://www.bilibili.com/video/{avs[0]['bvid']} 完成!!!")

reward_after = bilibili.get_reward()
add_content(f"投币获得经验：{reward_after['coins_av']}，分享视频{'成功' if reward_after['share_av'] else '失败'}!!!")
add_content(f"投币分享后等级：{reward_after['level_info']['current_level']}，投币分享后经验：{reward_after['level_info']['current_exp']}")

email.send(subject, content)
print('执行完成')
