import json
import random
import sys
import time

from msedge.selenium_tools import EdgeOptions, Edge
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def scroll_down_to_element(driver, element):
    # 向下滚动页面，每次滚动一个屏幕高度
    screen_height = driver.execute_script("return window.innerHeight")
    current_height = 0
    while True:
        driver.execute_script(f"window.scrollTo(0, {current_height});")
        current_height += screen_height
        if element.is_displayed():
            break
    # 将元素滚动到页面中心
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)


options = EdgeOptions()
options.add_argument('--headless')  # 不显示浏览器界面
options.add_argument('--disable-gpu')  # 禁用 GPU 加速，解决一些兼容性问题
options.add_argument('--window-size=1920,1080')
options.use_chromium = True
# 创建 Chrome 的 webdriver
driver = Edge(options=options)
# driver.maximize_window()
driver.get('https://www.bilibili.com/')
# 删除本次打开网页时的所有cookie
driver.delete_all_cookies()
with open('jsoncookie.json', 'r') as f:
    ListCookies = json.loads(f.read())
# 将jsoncookie.json里的cookie写入本次打开的浏览器中。
for cookie in ListCookies:
    driver.add_cookie({
        'domain': '.bilibili.com',
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None,
        'httponly': False,
    })
driver.get('https://www.bilibili.com/')
cont = 0
with open('抽奖地址.text', 'r', encoding='utf-8') as f:
    if f.read() == '没有近期开奖':
        print('没有近期开奖')
        sys.exit()
    else:
        for url in f.read().strip().split('\n'):

            # 转到抽奖地址
            driver.get(url)
            time.sleep(3)
            # 鼠标移动到头像上并停留5s
            touxiang = driver.find_element(By.CSS_SELECTOR,
                                           '#app > div.content > div > div > div.bili-dyn-item__main > div.bili-dyn-item__avatar > div > div > img')
            ActionChains(driver).move_to_element(touxiang).perform()
            time.sleep(3)
            # 判断是否关注
            # yiguanzhu = driver.find_element(By.CSS_SELECTOR,'body > div.bili-user-profile > div > div > div.bili-user-profile-view__info > div.bili-user-profile-view__info__footer > div.bili-user-profile-view__info__button.follow.checked')
            guanzhu = driver.find_element(By.CSS_SELECTOR,
                                          'body > div.bili-user-profile > div > div > div.bili-user-profile-view__info > div.bili-user-profile-view__info__footer > div.bili-user-profile-view__info__button.follow')

            # print(guanzhu.text)
            try:
                if guanzhu.text == '关注':
                    guanzhu.click()
                    time.sleep(1)
                ltguanzhu = driver.find_element(By.CLASS_NAME, 'dyn-orig-author__right')
                if ltguanzhu.text == '关注':
                    ltguanzhu.click()
                    time.sleep(1)

            except:
                pass
            # 定位到当前页面最底部的元素
            # element = driver.find_element(By.XPATH, '//footer')
            #
            # # 使用ActionChains模块将鼠标移动到该元素上
            # actions = ActionChains(driver)
            # actions.move_to_element(element).perform()
            #
            # # 等待一定时间，使得页面加载完毕
            # time.sleep(1)
            time.sleep(1)
            driver.execute_script("window.scrollBy(0, 300)")
            time.sleep(2)
            # 输入框
            inputbox = driver.find_element(By.XPATH,
                                           '//*[@id="app"]/div[2]/div/div/div[2]/div[2]/div/div[3]/div[2]/textarea')
            scroll_down_to_element(driver, inputbox)
            # inputbox_location = inputbox.location_once_scrolled_into_view  # 输入框位置
            # # 鼠标移动到输入框
            # actions = ActionChains(driver)
            # actions.move_by_offset(inputbox_location['x'], inputbox_location['y'])
            # actions.perform()
            try:  # 点赞
                dianzan = driver.find_element(By.CSS_SELECTOR, '.bili-dyn-action.like')
                if 'active' not in dianzan.get_attribute('class'):
                    dianzan.click()
                else:
                    pass
            except:
                pass

            time.sleep(1.5)
            # 预约
            try:
                yuyue = driver.find_element(By.CLASS_NAME, 'uncheck').click()
                time.sleep(2)

            except:
                pass
                # 转发
            zhuanfa = driver.find_element(By.CLASS_NAME, 'dynamic-repost-checkbox')

            if not zhuanfa.is_selected():
                # 如果未被选中，则点击它以勾选
                zhuanfa.click()
            time.sleep(2)

            # 发送文本
            lst = ['答案大所大所多', '谢谢自己万岁', '我中了', '给我中!']
            inputbox.click()
            time.sleep(1)
            inputbox.send_keys(lst[random.randint(0, 3)])
            time.sleep(1.5)
            driver.find_element(By.CLASS_NAME, 'comment-submit').click()
            time.sleep(2)
            cont += 1

            # 设置浏览器滚动条操作模拟
with open('cont.text', 'w', encoding='utf-8') as f:
    f.write('总共抽了{}次奖'.format(cont))
driver.close()
