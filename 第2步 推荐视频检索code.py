import requests
import re
import json
import traceback
import urllib.parse
import time
import datetime
import urllib.request

typical_video1 = []
typical_video2 = []
typical_video3 = []

class Throttle:

    def __init__(self, delay):
        # 访问同域名时需要的间隔时间
        self.delay = delay
        # key:netloc,value:lastTime.记录每个域名的上一次访问的时间戳
        self.domains = {}

    # 计算需要的等待时间，并执行等待
    def wait(self, url):
        if self.delay <= 0:
            print('delay ='+self.delay)
            return

        domain = urllib.parse.urlparse(url).netloc
        lastTime = self.domains.get(domain)

        if lastTime is not None:
            # 计算等待时间
            wait_sec = self.delay - (datetime.datetime.now() - lastTime).seconds
            if wait_sec > 0:
                time.sleep(wait_sec)

        self.domains[domain] = datetime.datetime.now()

#写表头
with open("D://related_videos_1.csv", "a", encoding='utf-8-sig') as f:
    f.write("up_id" + "," + "up_name" +  "," + "video_title" + "," + "video_av" + "," + "up_date" +"," + \
         "watch_num" +","+ "subtitle_num" +","+ "comment_num" +","+ "up_type" + "," +"\n")
    f.close()

#读取储存典型视频av号的txt，添加到列表typical_video1里
with open('D://typical_video.txt') as f:
    lines = f.readlines()
    for line in lines:
        line=line.strip("\n")
        typical_video1.append(line)

def gethtml(url):
    """
    请求html文本数据
    """
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = "utf-8"
    return r.text

def parsepage_step2(lst2, html):
    """
    解析视频页面源代码，提取“推荐视频”的信息
    """
    related_videos = re.findall(r'\"related\":\[{.*?}\]', html, re.S)
    for i in related_videos:
        i = "{" + i + "}"
        j = json.loads(i)
    for i in j["related"]:
        up_id = i["owner"]["mid"]
        up_name = i["owner"]["name"]
        video_title = i["title"]
        video_av = i["aid"]
        up_date = "unknown"
        watch_num = i["stat"]["view"]
        subtitle_num = i["stat"]["danmaku"]
        comment_num = "unknown"
        up_type = "C"
        with open("D://related_videos_1.csv", "a", encoding='utf-8-sig') as f:
            f.write(str(up_id)+"," + up_name+"," + video_title+"," + str(video_av)+","+up_date+"," + str(watch_num)\
                    +","+str(subtitle_num)+"," + comment_num +","+ up_type+"\n")
            f.close()
        lst2.append(str(video_av))
    return lst2

def step_2(lst1, lst2):
    count = 0
    t = Throttle(0.5)
    for i in lst1:
        try:
            url = "https://www.bilibili.com/video/av" + str(i)
            html = gethtml(url)
            t.wait(url)
            parsepage_step2(lst2, html)
            count += 1
            print("\r当前速度:{:.2f}%".format(count * 100 / len(lst1)), end="")
        except:
            traceback.print_exc()
            continue


print(len(typical_video1))
step_2(typical_video1, typical_video2)
step_2(typical_video2, typical_video3)
print("\n" + str(len(typical_video3)))
