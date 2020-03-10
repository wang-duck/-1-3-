import json
import numpy as np
import pandas as pd
import jieba
from nltk import FreqDist
import wordcloud
from matplotlib import pyplot as plt

#读取json文件：方法一
# with open("C:\\Users\\yeyuexiaoqi\\PycharmProjects\\untitled1\\RGF\\output.json",'r') as load_f:
#     load_dict = json.load(load_f)
#     # print(load_dict)
# df = pd.DataFrame(load_dict)
# print(df)

#读取json文件：方法二
df = pd.read_json("C:\\Users\\yeyuexiaoqi\\PycharmProjects\\untitled1\\RGF\\output.json", orient="records")
for i in range(26774):
    df.iloc[i, 18] = "#".join(df.iloc[i, 18]).strip("\n").strip("  ")
    df.iloc[i, 19] = "#".join(df.iloc[i, 19]).strip("\n").strip("  ")

df1 = df.iloc[:, 0:18]  #所有数据的前18列（因为“福利待遇”和“职位详述”文字较多，暂时剔除）
df2 = df[df["招聘状态"]=="应聘"]  #切取正在招聘中的岗位

#将df1和df2保存到excel表里，方便之后查看。存完不再用得到了，所以注释掉
# df1.to_excel('df1.xlsx', sheet_name='Sheet1')
# df2.to_excel('df2.xlsx', sheet_name='Sheet1')

#将正在招聘中的“职位名”提取出来，转换为列表
position_list = df["职位名"].tolist()
print(len(position_list))

#对"职位名"进行切词处理
position_wordcut = []
for i in position_list:
    try:
        wordcuts = jieba.lcut(i)
        position_wordcut += wordcuts
    except:
        print(i)
        pass

#统计切词后的词频，保存到字典freq1里
freq = FreqDist(position_wordcut)
freq1={}
for k in freq:
    if len(k)>=2 and freq[k]>1:  #删掉长度为1的词，和词频为1的词
        freq1[k]=freq[k]
#删除几个无关痛痒的词
del freq1["编号"]
del freq1["日企"]
del freq1["日语"]
del freq1["担当"]

print(freq1)

# 绘制“职位名”词频云图
ccloud = wordcloud.WordCloud(background_color='white', width=1600, height=800, font_path='C:\\Windows\WinSxS\\amd64_microsoft-windows-font-truetype-dengxian_31bf3856ad364e35_10.0.18362.1_none_2f009e78b33b73a9\\Dengb.ttf')
ccloud.generate_from_frequencies(frequencies=freq1)
plt.figure()
plt.imshow(ccloud, interpolation="bilinear")
plt.axis('off')
plt.show()










