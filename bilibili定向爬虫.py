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


#以下为STEP 2的代码。

def getapi(url):
    """
    请求动态网页数据，以json格式返回
    """
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        r_json = r.json()
        return r_json
    except:
        print("产生异常")

def get_videoinfo(r_json):
    """
    从up主的空间，获取其投稿的所有视频的信息。包括标题、播放量、评论数等等
    保存到space_videos_list.csv文件中
    """
    vlist = r_json["data"]["list"]["vlist"]
    for i in vlist:
        up_id = i.get("mid")
        up_name = i.get("author")
        video_title = i.get("title")
        video_av = i.get("aid")
        up_date = i.get("created")
        watch_num = i.get("play")
        subtitle_num = "unknown"
        comment_num = i.get("comment")
        up_type = "B"
        with open("D://space_videos_list.csv", "a", encoding='utf-8-sig') as f:
            f.write(str(up_id) + "," + up_name + "," + video_title + "," + str(video_av) + "," + str(up_date) + "," + str(watch_num)\
                    + "," + str(subtitle_num) + "," + str(comment_num) + "," + up_type + "\n")
    return

def step_2():
    """
    把step1中获得的up_id去除重复项后，访问up主的空间，并爬取up投稿的所有视频信息
    :url1: 此链接可获取up主上传的视频总数（主要为了通过视频总数，判断在视频页应该爬取几页）
    :url2：所有视频页
    """
    count = 0
    url1_base = "https://api.bilibili.com/x/space/navnum?jsonp=jsonp&mid="
    url2_base = "https://api.bilibili.com/x/space/arc/search?ps=100&jsonp=jsonp"
    midlist_set = list(set(midlist))
    print("length of the midlist_set:" + str(len(midlist_set)))
    for mid in midlist_set:
        count += 1
        url1 = url1_base + str(mid)
        r_json1 = getapi(url1)
        video_num = r_json1["data"]["video"]
        pn = int(video_num/100) + 1
        for i in range(1,pn+1):
            url2 = url2_base + "&pn=" + str(pn) + "&mid=" + str(mid)
            r_json2 = getapi(url2)
            get_videoinfo(r_json2)
        print("\r当前速度:{:.2f}%".format(count * 100 / len(midlist_set)), end="")
    print(" \nstep2 is finished")


write_filetitle("D://doctor_key_search.csv")
write_filetitle("D://space_videos_list.csv")
step_1()
step_2()



