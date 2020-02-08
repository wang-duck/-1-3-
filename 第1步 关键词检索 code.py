import requests
import re
import traceback
import json

midlist = []

def write_filetitle(filename):
    with open(filename, "a", encoding='utf-8-sig') as f:
        f.write("up_id" + "," + "up_name" +  "," + "video_title" + "," + "video_av" + "," + "up_date" +"," + \
            "watch_num" +","+ "subtitle_num" +"," + "comment_num" +","+ "up_type" + "," +"\n")


#以下为STEP 1的代码
def gethtml(url):
    """
    请求html文本数据
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "产生异常"

def parsepage_step1(html):
    """
    解析html页面，获取相关信息并储存到doctor_key_search.csv文件中。
    同时将up主的id，储存到midlist列表中

    :param html: 通过url请求到的html页面文本
    :return: 返回up主的id列表
    """
    try:
        up_links = re.findall(r'a href=\"//space.bilibili.com/.*?\"', html)
        up_names = re.findall(r'up-name\">.*?</a>', html)
        video_titles = re.findall(r'<a title=\".*?\"', html)
        video_links = re.findall(r'a href=\"//www.bilibili.com/video/av.*?\"', html)
        up_dates = re.findall(r'icon-date\"></i>.*?</span>', html, re.S)
        watch_nums = re.findall(r'icon-playtime\"></i>.*?</span>', html, re.S)
        subtitle_nums = re.findall(r'icon-subtitle\"></i>.*?</span>', html, re.S)
        for i in range(len(video_titles)):
            up_id = re.split(r'com/|\?from=search"', up_links[i])[1]
            up_name = re.split(r'">|</', up_names[i])[1]
            video_title = video_titles[i].split('"')[1]
            video_av = re.split(r'video/|\?from=search"', video_links[i])[1]
            up_date = re.split(r'\n', up_dates[i])[1]
            watch_num = re.split(r'\n', watch_nums[i])[1]
            subtitle_num = re.split(r'\n', subtitle_nums[i])[1]
            comment_num = "unknown"
            up_type = "A"
            with open("D://doctor_key_search.csv", "a", encoding='utf-8-sig') as f:
                f.write(str(up_id) + "," + up_name + "," + video_title + "," + str(video_av) + "," + up_date + "," + str(watch_num)\
                    + "," + str(subtitle_num) + "," + comment_num + "," + up_type + "\n")
            midlist.append(str(up_id))
        return midlist
    except:
        print("产生异常")

def step_1():
    """
    以博士为关键词，请求50页的数据。print打印页面爬取进度
    """
    kw = "博士"
    page = 50
    count = 0
    start_url = "https://search.bilibili.com/all?keyword=" + str(kw) + "&from_source=nav_search_new&page="
    for i in range(page):
        try:
            url = start_url + str(i+1)
            html = gethtml(url)
            parsepage_step1(html)
            count += 1
            print('\rSTEP 1正在进行:{:.2f}%'.format(count * 100 /page), end="")
        except:
            count += 1
            print('\rSTEP 1正在进行:{:.2f}%'.format(count * 100 / page), end="")
            traceback.print_exc()
            continue
    print("\nstep1 is finished\n")

write_filetitle("D://doctor_key_search.csv")
step_1()