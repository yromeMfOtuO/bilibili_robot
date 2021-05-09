import requests
import json


class BilibiliClient(object):
    # B站web的api接口

    __headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36",
        "Referer": "https://www.bilibili.com/"
    }

    def __init__(self, config):
        if config is None or config.properties['bilibiliCookies'] is None:
            raise Exception('获取邮箱配置失败')
        self.__cookieData = config.properties['bilibiliCookies']
        # 创建session
        self.__session = requests.session()
        # 添加cookie
        requests.utils.add_dict_to_cookiejar(self.__session.cookies, self.__cookieData)
        # 设置header
        self.__session.headers.update(BilibiliClient.__headers)

        self.__bili_jct = self.__cookieData["bili_jct"]
        self.__uid = self.__cookieData["DedeUserID"]

        content = self.__session.get("https://account.bilibili.com/home/reward")
        if json.loads(content.text)["code"] != 0:
            raise Exception("参数验证失败，登录状态失效")

    def get_reward(self):
        # 取B站经验信息
        url = "https://account.bilibili.com/home/reward"
        content = self.__session.get(url)
        return json.loads(content.text)["data"]

    def get_coin(self):
        # 获取剩余硬币数
        url = "https://api.bilibili.com/x/web-interface/nav?build=0&mobi_app=web"
        content = self.__session.get(url)
        return int(json.loads(content.text)["data"]["money"])

    def add_coin(self, aid, num, select_like):
        # 给指定av号视频投币
        url = "https://api.bilibili.com/x/web-interface/coin/add"
        post_data = {
            "aid": aid,
            "multiply": num,
            "select_like": select_like,
            "cross_domain": "true",
            "csrf": self.__bili_jct
        }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def share(self, aid):
        # 分享指定av号视频
        url = "https://api.bilibili.com/x/web-interface/share/add"
        post_data = {
            "aid": aid,
            "csrf": self.__bili_jct
        }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def report(self, aid, cid, progres):
        # B站上报观看进度
        url = "http://api.bilibili.com/x/v2/history/report"
        post_data = {
            "aid": aid,
            "cid": cid,
            "progres": progres,
            "csrf": self.__bili_jct
        }
        content = self.__session.post(url, post_data)
        return json.loads(content.text)

    def get_home_page_urls(self):
        # 取B站首页推荐视频地址列表
        import re
        url = "https://www.bilibili.com"
        content = self.__session.get(url)
        match = re.findall('<div class=\"info-box\"><a href=\"(.*?)\" target=\"_blank\">', content.text, 0)
        match = ["https:" + x for x in match]
        return match

    @staticmethod
    def get_regions(rid=1, num=6):
        # 获取B站分区视频信息
        url = "https://api.bilibili.com/x/web-interface/dynamic/region?ps=" + str(num) + "&rid=" + str(rid)
        content = requests.get(url, headers=BilibiliClient.__headers)
        data = json.loads(content.text)["data"]["archives"]
        ids = []
        for x in data:
            ids.append({"title": x["title"], "aid": x["aid"], "bvid": x["bvid"], "cid": x["cid"]})
        return ids

