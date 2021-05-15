from services.bilibili_client import BilibiliClient
from services.config import Config
from os import linesep

content = ""

config = Config()
config.print()
bilibili = BilibiliClient(config)
reward = bilibili.get_reward()
print(reward)
avs = bilibili.get_regions(rid=20, num=5)
print(avs)
share = bilibili.share(avs[0]['aid'])
print(share)

def add_content(line):
    global content
    content = content.__add__(line).__add__(linesep)

reward_after = bilibili.get_reward()
add_content(f"投币获得经验：{reward_after['coins_av']}，分享视频{'成功' if reward_after['share_av'] else '失败'}!!!")
add_content(f"当前等级：{reward_after['level_info']['current_level']}，当前经验：{reward_after['level_info']['current_exp']}")

print(content)