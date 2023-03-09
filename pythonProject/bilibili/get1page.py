from bs4 import BeautifulSoup
import requests
import re
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
date_file_0 = os.path.join(script_dir, '抽奖网址0.text')
date_file_1 = os.path.join(script_dir, '抽奖地址1.text')

with open(date_file_0, mode='r', encoding='utf-8') as f:
    url = f.read()
    if url == '没有近期开奖':
        with open(date_file_1, mode='w', encoding='utf-8') as f:
            f.write(url)
        sys.exit()
    else:

        htmls = requests.get(
            url=url
        )
        soup = BeautifulSoup(htmls.text, 'html.parser')

        list1 = soup.find_all(name='a', attrs={"class": 'article-link'})
        url0 = []
        for a in list1:
            link2 = a.text
            link2 = re.findall(r"(?i)\b((?:https?://|ftp://|www\.)\S+)\b", link2)
            url0.append(link2[0])
        print(url0)
        with open(date_file_1, mode='w', encoding='utf-8') as f:
            for i in url0:
                if i == 'https://t.bilibili.com/635932563238551585?tab=2':
                    continue
                new_url = re.sub(r"https://www.bilibili.com/opus/", "https://t.bilibili.com/", i)
                f.write(new_url + '\n')
