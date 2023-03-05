import os
import time
import subprocess

subprocess.call([r'python', r'G:\pyxiangmu\pythonProject\pythonProject\bilibili\get0page.py'])
time.sleep(2)
subprocess.call([r'python', r'G:\pyxiangmu\pythonProject\pythonProject\bilibili\get1page.py'])
time.sleep(2)
# os.system(r'python G:\pyxiangmu\pythonProject\pythonProject\bilibili\cookieget.py')
# time.sleep(5)
subprocess.call([r'python', r'G:\pyxiangmu\pythonProject\pythonProject\bilibili\cookielogin.py'])
