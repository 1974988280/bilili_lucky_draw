from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from msedge.selenium_tools import EdgeOptions, Edge
import os

options = EdgeOptions()
options.add_argument('--headless')  # 不显示浏览器界面
options.add_argument('--disable-gpu')  # 禁用 GPU 加速，解决一些兼容性问题
options.use_chromium = True
# 创建 Chrome 的 webdriver
driver = Edge(options=options)

# 打开目标网站
url = 'https://space.bilibili.com/226257459/article'
driver.get(url)
# html = driver.page_source  # 网页源码

# print(html)
# 等待页面加载完成
wait = WebDriverWait(driver, 5)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.article-wrap li')))

# 查找 <h2> 元素下的所有 <a> 元素
li_tags = driver.find_elements(By.CSS_SELECTOR, 'h2.article-title a')

# 获取第一个数据并判断是否为近期开奖
a_element = driver.find_element(By.CSS_SELECTOR, 'h2.article-title a')
a_href = a_element.get_attribute('href')
first1 = li_tags[0].text

if '近期开奖' in first1:
    with open('抽奖网址.text', mode='w', encoding='utf-8') as f:
        f.write(a_href)
else:
    with open('抽奖网址.text', mode='w', encoding='utf-8') as f:
        f.write("没有近期开奖")

# 输出每个 <li> 元素的文本内容
# for li in li_tags:
#     print(li.text)
#


# 关闭浏览器
driver.quit()
# if '近期开奖' in first1:
#     print(first1)
