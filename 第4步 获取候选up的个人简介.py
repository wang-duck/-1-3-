import requests
import xlsxwriter

wb = xlsxwriter.Workbook('D://up_info.xlsx')  # 建立工作簿
ws = wb.add_worksheet()
ws.set_row(0, 45)  # 设置行高
headData = ['up_id', 'up_name', 'up_intro', 'up_space_url']
for colnum in range(0, 4):
    ws.write(0, colnum, headData[colnum])    #写表头

midlist = []


with open('D://up_id.txt') as f:
    lines = f.readlines()
    for line in lines:
        line=line.strip("\n")
        midlist.append(line)

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

def get_upinfo(lst, html):
    """
    从up主的空间主页获取粉丝数量和自我简介信息
    """
    data = html.get("data")
    up_id = data.get("mid")
    up_name = data.get("name")
    up_intro = data.get("sign")
    lst.append(str(up_id))
    lst.append(up_name)
    lst.append(up_intro)

def up_info():
    """
    获取up主简介，并保存到excel表里
    """
    for i in range(len(midlist)):
        try:
            info_list = []
            mid = midlist[i]
            url1_base = "https://api.bilibili.com/x/space/acc/info?jsonp=jsonp&mid="
            url1 = url1_base + str(mid)
            html1 = gethtml(url1)
            get_upinfo(info_list, html1)
            up_url = "https://space.bilibili.com/" + str(mid) + "/video"
            info_list.append(up_url)
            for colnum in range(0, 4):
                ws.write(i + 1, colnum, info_list[colnum])  # 将up信息保存到xlsx表里
            print("\r当前速度:{:.2f}%".format((i + 1) * 100 / len(midlist)), end="")
        except:
            print("\nThere is something wrong with " + str(i+1))
            continue
    wb.close()
    print(" \nstep4 is finished")


print(len(midlist))
up_info()
