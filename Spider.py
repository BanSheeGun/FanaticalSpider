#!/usr/bin/python
# -*- coding: UTF-8 -*-

from selenium import webdriver
from bs4 import BeautifulSoup
import xlwt


def get_page_soup(url):
    """
    :param url: 页面 url
    :return: 页面内容
    """
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    return soup


def game_spider(url, bundle_name):
    """
    :param url:慈善包页面 url
    :param bundle_name: 慈善包包名
    :return: 慈善包所包含的游戏
    """
    res = []
    soup = get_page_soup(url)
    games_tags = soup.find_all("p", class_="text-truncated m-0")
    print("find %d game(s) in" % len(games_tags), bundle_name)
    name = [x.contents[1] for x in games_tags]
    price = [x.contents[4].text for x in games_tags]
    for a, b in zip(name, price):
        res.append([a, b])
    return res


def bundle_spider(url):
    """
    :param url:Fanatical 的 url
    :return: 页面包含的慈善包
    """
    res = []
    soup = get_page_soup(url)
    bundle_tags = soup.find_all('a', class_="faux-block-link__overlay-link")
    print("find %d bundle(s)" % len(bundle_tags))
    prices_tag = soup.find_all('div', class_=' hitCardStripe d-flex justify-content-end' +
                                             ' justify-content-md-between align-items-center card-block')
    price = [x.contents[1].next.text for x in prices_tag]
    name = [x.next.next for x in bundle_tags]
    burl = [Fanatical + x['href'] for x in bundle_tags]
    game = [game_spider(x, y) for x, y in zip(burl, name)]
    for a, b, c, d in zip(name, price, burl, game):
        res.append([a, b, c, d])
    return res


def output_to_excel():
    """
    :return:将所有信息保存到 xls 文件中
    """
    wbk = xlwt.Workbook()
    bundle_sheet = wbk.add_sheet("Bundle")
    game_sheet = wbk.add_sheet("Game")
    bundle_sheet.col(0).width = 9000
    bundle_sheet.col(1).width = 6000
    bundle_sheet.col(2).width = 18000
    game_sheet.col(0).width = 12000
    game_sheet.col(1).width = 6000

    cols = 0
    for bundle in Bundles:
        bundle_sheet.write(cols, 0, bundle[0])
        bundle_sheet.write(cols, 1, bundle[1])
        bundle_sheet.write(cols, 2, bundle[2])
        cols += 1

    cols = 0
    for bundle in Bundles:
        game_sheet.write(cols, 0, bundle[0])
        cols += 1
        for game in bundle[3]:
            game_sheet.write(cols, 0, game[0])
            game_sheet.write(cols, 1, game[1])
            cols += 1
        cols += 2

    wbk.save("D:\\1.xls")


Fanatical = "https://www.fanatical.com"
BundlePage = "https://www.fanatical.com/en/bundle"
options = webdriver.FirefoxOptions()  # 初始化浏览器
options.add_argument('-headless')
driver = webdriver.Firefox(firefox_options=options)

Bundles = bundle_spider(BundlePage)  # 爬取页面信息
output_to_excel()  # 保存信息
driver.close()  # 关闭浏览器
