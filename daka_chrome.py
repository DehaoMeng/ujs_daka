#!/usr/bin/python3
# @File: daka.py
# --coding: utf-8--
# @Author: 昊昊反思
# @Time: 2022年 03月 30日 11:55
"""
说明: 江苏大学自动健康打开 目前只实现了输入温度和无异常功能
"""
import selenium
from ddddocr import DdddOcr
import tkinter as tk
import tkinter.messagebox
import requests
from PIL import Image
from hashlib import md5
from selenium import webdriver
from time import sleep
# 实现规避检测
# 实现无可视化界面
from selenium.webdriver.chrome.options import Options


def Daka(name, pwd):
    # 风险规避
    # 无可视化操作
    option = Options()
    option.add_experimental_option('excludeSwitches', ['enable-automation'])
    option.add_argument('--headless')
    option.add_argument('--disable-gpu')
    option.add_argument('window-size=1920x1080')
    bro = webdriver.Chrome(options=option)
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
    """ 需要进行更改坐标 """
    location['x'] = 1250
    location['y'] = 329
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
    print(code)

    try:
        username = bro.find_element_by_id('username')
        password = bro.find_element_by_id('password')

        username.send_keys(name)
        password.send_keys(pwd)

        yanzhengma_word = bro.find_element_by_id('captchaResponse')
        yanzhengma_word.send_keys(code)
        print("输入成功")
        btn_login = bro.find_element_by_class_name('auth_login_btn')
        btn_login.click()
        sleep(1)
        bro.find_element_by_class_name('weui_btn').click()
    except :
        tk.messagebox.showinfo(title='提示', message='账号密码或验证码错误，请重新输入或者再试一次')
        exit(0)

    bro.find_element_by_class_name('weui_btn').click()

    print('点击成功')

    sleep(1)
    try:
        yesterday = bro.find_element_by_id('xwwd')
    except:
        tk.messagebox.showinfo(title='提示', message='超过正常打卡时间。')
        exit(0)
    yesterday.send_keys('36')
    today = bro.find_element_by_id('swwd')
    today.send_keys('36')
    bro.find_element_by_xpath('//*[@id="qtyc"]/option[2]').click()
    btn_submit = bro.find_element_by_id('button1')
    btn_submit.click()
    bro.quit()

    root = tk.Tk()
    root.withdraw()
    tkinter.messagebox.showinfo(title='提示', message='打卡成功')
