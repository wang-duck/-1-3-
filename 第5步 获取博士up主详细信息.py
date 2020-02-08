import requests
import xlsxwriter
import urllib.parse
import time
import datetime
import urllib.request

wb = xlsxwriter.Workbook('D://up_info.xlsx')  # 建立工作簿
ws = wb.add_worksheet()
ws.set_row(0, 45)  # 设置行高
headData = ['up_id', 'up_name', 'up_sex', 'up_intro', 'up_level', 'up_birthday', 'up_fans', 'up_videonum', 'up_space_url','up_face']
for colnum in range(0, 10):
    ws.write(0, colnum, headData[colnum])    #写表头

midlist = []


with open('D://up_id.txt') as f:
    lines = f.readlines()
    for line in lines:
        line=line.strip("\n")
        midlist.append(line)

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

def gethtml(url):
    """
    请求html文本数据
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.json()
        return html
    except:
        return "产生异常"

def getpic(url):
    """
     通过up主头像链接，获取up主头像
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.content
    except:
        return "产生异常"


def get_upinfo(lst, suffix_lst, html):
    """
    从up主的空间主页获取粉丝数量和自我简介信息
    """
    data = html.get("data")
    up_id = data.get("mid")
    up_name = data.get("name")
    up_sex = data.get("sex")
    up_intro = data.get("sign")
    up_level = data.get("level")
    up_birthday = data.get("birthday")
    up_face_url = data.get("face")
    up_face = getpic(up_face_url)
    lst.append(str(up_id))
    lst.append(up_name)
    lst.append(up_sex)
    lst.append(up_intro)
    lst.append(str(up_level))
    lst.append(str(up_birthday))
    pic_suffix = up_face_url.split(".")[-1]
    suffix_lst.append(pic_suffix)
    with open("D://up_pic//"+str(up_id)+"."+pic_suffix, "wb") as f:
        f.write(up_face)
    return lst

def get_followers(lst,html):
    """
    获取up主的粉丝数量
    """
    data = html.get("data")
    up_fans = data.get("follower")
    lst.append(str(up_fans))
    return up_fans

def get_videonum(lst,html):
    """
    获取up主投稿的视频总数
    """
    data = html.get("data")
    up_videonum = data.get("video")
    lst.append(str(up_videonum))
    return up_videonum

def up_info():
    """
    获取up主各项信息，并保存到excel表里
    """
#    t = Throttle(0.5)  #此处t可以设置小一点。
    for i in range(len(midlist)):
        try:
            info_list = []
            suffix_list = []
            mid = midlist[i]
            url1_base = "https://api.bilibili.com/x/space/acc/info?jsonp=jsonp&mid="
            url1 = url1_base + str(mid)
            html1 = gethtml(url1)
#            t.wait(url1)
            get_upinfo(info_list, suffix_list, html1)
            url2_base = "https://api.bilibili.com/x/relation/stat?jsonp=jsonp&vmid="
            url2 = url2_base + str(mid)
            html2 = gethtml(url2)
#            t.wait(url2)
            get_followers(info_list, html2)
            url3_base = "https://api.bilibili.com/x/space/navnum?jsonp=jsonp&mid="
            url3 = url3_base + str(mid)
            html3 = gethtml(url3)
#            t.wait(url3)
            get_videonum(info_list, html3)
            up_url = "https://space.bilibili.com/" + str(mid) + "/video"
            info_list.append(up_url)
            ws.set_row(i + 1, 45)  # 设置行高
            for colnum in range(0, 9):
                ws.write(i + 1, colnum, info_list[colnum])  # 将除up头像以外的信息保存到xlsx表里
            param = {
                'x_offset': 0,
                'y_offset': 1 * 60,
                'x_scale': 0.09,
                'y_scale': 0.09,
                "width": 20,
                "height": 20,
                'url': None,
                'tip': None,
                'image_data': None,
                'positioning': None,
            }
            if suffix_list[0] == "gif":
                ws.insert_image('J' + str(i + 1), "D://up_pic//noface.png", param)
            else:
                ws.insert_image('J' + str(i + 1), "D://up_pic//" + str(mid) + "." + suffix_list[0], param)
            print("\r当前速度:{:.2f}%".format((i + 1) * 100 / len(midlist)), end="")
        except:
            print("\nThere is something wrong with " + str(i+1))
            continue
    wb.close()
    print(" \nstep4 is finished")

print(len(midlist))
up_info()


