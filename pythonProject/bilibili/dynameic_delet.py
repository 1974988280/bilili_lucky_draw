import time
import os
import json
from datetime import datetime
from selenium.webdriver import Edge, EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

# 路径
script_dir = os.path.dirname(os.path.abspath(__file__))
# date_file_0 = os.path.join(script_dir, '抽奖网址0.text')
# date_file_1 = os.path.join(script_dir, '抽奖地址1.text')
date_file_cont = os.path.join(script_dir, 'cont_delete.text')
date_file_json = os.path.join(script_dir, 'jsoncookie1.json')
options = EdgeOptions()

# 配置浏览器设置
options.add_argument('--headless')  # 不显示浏览器界面
options.add_argument('--disable-gpu')  # 禁用 GPU 加速，解决一些兼容性问题
options.add_argument('--window-size=1920,1080')
options.use_chromium = True

driver = Edge(options=options)
driver.get('https://space.bilibili.com/1242917617/dynamic')
# 导入cookies
with open(date_file_json, 'r') as f:
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
# 打开动态页
driver.get('https://space.bilibili.com/1242917617/dynamic')
time.sleep(3)
# 删除动态,数量为cont_delete
cont_delete = 0
now = datetime.now()
now_str = now.strftime('%m-%d %H:%M')
cont_list = 0

try:
    while cont_delete < 469:
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.bili-dyn-more__btn.tp')))
        load_more_button.click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'div[data-module="more"][data-type="THREE_POINT_DELETE"]').click()
        time.sleep(1.5)
        driver.find_element(By.CSS_SELECTOR,
                            'body > div.bili-modal__wrap > div.bili-modal > div.bili-modal__footer > button.bili-modal__button.confirm').click()
        time.sleep(1.5)
        cont_delete += 1
        cont_list += 1
        # 加载数据
        if cont_list != 0 and cont_list % 10 == 0:
            js_script = "window.scrollBy(0, 1000);"
            driver.execute_script(js_script)
            time.sleep(2)
            js_script = "window.scrollBy(0, -1000);"
            driver.execute_script(js_script)
            if cont_list % 11 == -1:
                cont_list = 0

except:
    pass
with open('cont_delete', 'a', encoding='utf-8') as f:
    f.write('{}总共删除了{}条动态\n'.format(now_str, cont_delete))
