#!/usr/bin/python3
# @File: daka.py
# --coding: utf-8--
# @Author: 昊昊反思
# @Time: 2022年 03月 30日 11:55
"""
说明:
"""
from ddddocr import DdddOcr
import time
import tkinter as tk
import tkinter.messagebox
import requests
from PIL import Image
from hashlib import md5
from selenium import webdriver
from lxml import etree
from time import sleep
# 实现规避检测
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
# 实现无可视化界面
from selenium.webdriver.edge.options import Options


#
def login_in(self, bro):
    self.bro.find_element_by_class_name('weui_btn').click()
    print('点击成功')


if __name__ == "__main__":
    # 风险规避
    option = EdgeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 无可视化操作
    caps = {
        "browserName": "MicrosoftEdge",
        "version": "",
        "platform": "WINDOWS",
        # 关键是下面这个
        "ms:edgeOptions": {
            'extensions': [],
            'args': [
                '--headless',
                '--disable-gpu'
            ]}
    }
    # UA伪装
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'
    }
    # 网页页面获取
    bro = webdriver.Edge(executable_path='./msedgedriver.exe', capabilities=caps)
    # bro = Edge(executable_path='./msedgedriver', capabilities=EDGE,options=option)
    # bro = Edge(executable_path='./msedgedriver', options=option)
    bro.get('https://pass.ujs.edu.cn/cas/login?service=http%3A%2F%2Fyun.ujs.edu.cn%2Fxxhgl%2Fyqsb%2Findex')
    # 页面最大化
    bro.maximize_window()
    # 获取页面内验证码图片 但是获取时会进行刷新图片 所以不可取
    # page_text = bro.page_source
    # tree = etree.HTML(page_text)
    # yanzheng_img_url ='https://pass.ujs.edu.cn/cas/'+tree.xpath('//*[@id="captchaImg"]/@src')[0]
    # yanzheng_img = requests.get(url=yanzheng_img_url,headers=headers).content
    # img_path = '验证码.jpg'
    # with open(img_path,'wb') as fp:
    #     fp.write(yanzheng_img)
    # 将当前页面进行截图(可行)
    bro.save_screenshot('aa.png')
    # 裁剪验证码区域图片（坐标）
    code_img_ele = bro.find_element_by_xpath('//*[@id="captchaImg"]')
    # 获取标签坐标
    location = code_img_ele.location
    size = code_img_ele.size
    # 裁剪不符合时，重新定坐标
    location['x'] = 640
    location['y'] = 330
    size['width'] = 94
    size['height'] = 31
    print('location', location)
    print('size', size)
    rangle = (
        location['x'], location['y'], location['x'] + size['width'], location['y'] + size['height']
    )
    i = Image.open('./aa.png')
    code_img_name = '验证码.png'
    frame = i.crop(rangle)
    frame.save(code_img_name)
    with open('验证码.png', 'rb') as f:
        img_bytes = f.read()
    ocr = DdddOcr()
    code = ocr.classification(img_bytes)

    username = bro.find_element_by_id('username')
    password = bro.find_element_by_id('password')

    username.send_keys('您的一卡通号')
    password.send_keys('您的密码')

    yanzhengma_word = bro.find_element_by_id('captchaResponse')
    yanzhengma_word.send_keys()
    print("输入成功")

    btn_login = bro.find_element_by_class_name('auth_login_btn')
    btn_login.click()

    time.sleep(10)

    bro.find_element_by_class_name('weui_btn').click()

    bro.find_element_by_class_name('weui_btn').click()

    print('点击成功')
    # # print(btn_insert)
    # btn_insert.click()
    # print(bro.current_url)

    # time.sleep(30)
    # bro.get(bro.current_url)
    time.sleep(5)
    yesterday = bro.find_element_by_id('xwwd')
    yesterday.send_keys('36')
    today = bro.find_element_by_id('swwd')
    today.send_keys('36')
    bro.find_element_by_xpath('//*[@id="qtyc"]/option[2]').click()
    # time.sleep(10)
    btn_submit = bro.find_element_by_id('button1')
    btn_submit.click()
    bro.quit()
    # print("打卡成功")
    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title='提示', message='打卡成功')
