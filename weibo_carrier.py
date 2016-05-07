#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#                       __
# \  /\  / _    /      /    _          _
#  \/  \/ (- / /) ()  /__  (/ /- /- / (- /-

import os
import re
import time
import requests
from lxml import etree
from PIL import Image, ImageDraw, ImageFont

# Layout
# Material style with colored date bar
LAYOUT_ONE = {'date_size': 145, 'post_size': 52, 'date_site': (20, -25), 'text_site': (40, 335),
              'post_spacing': 26, 'date_spacing': -5, 'line_sum': 8, 'line_interval': 87, 'LAYOUT_ONE': None}
# Material style with colored background
LAYOUT_TWO = {'date_size': 145, 'post_size': 52, 'date_site': (20, -25), 'text_site': (40, 335),
              'post_spacing': 26, 'date_spacing': -5, 'line_sum': 8, 'line_interval': 87, 'LAYOUT_TWO': None}
# Regular style
LAYOUT_THREE = {'date_size': 48, 'post_size': 50, 'date_site': (65, 60), 'text_site': (65, 190),
                'post_spacing': 26, 'line_sum': 10, 'line_interval': 85}  # (65, 200) 28  4/25

# Color scheme
# Recommend LAYOUT_ONE, LAYOUT_TWO, LAYOUT_THREE
LIGHT_GREY = {'bg': '#9E9E9E', 'text': '#FFFFFF'}
RED = {'bg': '#EF9A9A', 'text': '#FFFFFF'}
PINK = {'bg': '#F48FB1', 'text': '#FFFFFF'}
PURPLE = {'bg': '#CE93D8', 'text': '#FFFFFF'}
BLUE = {'bg': '#90CAF9', 'text': '#FFFFFF'}
CYAN = {'bg': '#80DEEA', 'text': '#FFFFFF'}
TEAL = {'bg': '#80CBC4', 'text': '#FFFFFF'}
GREEN = {'bg': '#A5D6A7', 'text': '#FFFFFF'}
ORANGE = {'bg': '#FFAB91', 'text': '#FFFFFF'}
BROWN = {'bg': '#BCAAA4', 'text': '#FFFFFF'}
# Recommend LAYOUT_TWO, LAYOUT_THREE
YELLOW = {'bg': '#FFFAE9', 'text': '#584A3C'}
WHITE = {'bg': '#FFFFFF', 'text': '#212121'}
DARK_GREY = {'bg': '#424242', 'text': '#FFFFFF'}
BLACK = {'bg': '#000000', 'text': '#FFFFFF'}

CH_PUN = ['”', '’', '，', '。', '、', '：', '；', '！', '？', '）', '】', '}', '》']
EN_PUN = ['"', "'", ',', '.', ':', ';', '!', '?', ')', ']', '}', '>']

LAYOUT = LAYOUT_ONE
COLOR_SCHEME = LIGHT_GREY
FONT = 'NotoSansCJKsc-DemiLight.otf'  # NotoSansCJKsc-DemiLight.otf  NotoSansCJKsc-Light.otf  NotoSansMonoCJKsc-Regular.otf

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36',
          'cookie': ''}
URL = ['']

EASY_READ = True
page_counter = 0
session = requests.session()


def print_log(*args, name='log_' + time.strftime('%y_%m'), cout=True, log=True):
    """print and save log to a file
    Args:
        *args:what to print
        name:name of the log file
        cout:print to screen or not
        log:log or not
    """
    if cout:
        print(''.join(args))
    if log:
        with open(os.path.abspath('.') + '\\%s.txt' % name, 'a', errors='ignore') as f:
            f.write('\n' + ''.join(args))


def timer(sec):
    """a timer that delay s secs

    Args:
        sec:delay s sec
    """
    print_log('\n-----rest for %s sec-----' % sec)
    time.sleep(sec)


def cut_line(string, point, reverse=False):
    """get the front or behind fragment of the line
    Args:
        string: string to cut
        point: point to stop
        reverse:return the behind fragment

    Returns:
        string
    """
    counter = 0
    for x in string:
        if x == point:
            break
        else:
            counter += 1
    if not reverse:
        return string[:counter]
    elif reverse:
        return string[counter + 1:]


def url_interpreter(url):
    """make a  url executable
    Args:
        url:original url

    Returns:
        url
    """
    if 'weibo.com' in url:
        if url.startswith('http://weibo.com/'):
            pass
        elif url.startswith('weibo.com/'):
            url = 'http://' + url
        else:
            raise ValueError('URL错误，请检查输入的URL是否为用户主页地址')
        source = session.get(url, headers=HEADER).text
        try:
            oid = re.findall(r"oid']='(.*?)'", source, re.S)[0]
        except IndexError:
            raise ConnectionError('Cookie可能已过期，请更新后再次尝试连接')
        url = 'http://weibo.cn/u/%s' % oid
    elif 'weibo.cn' in url:
        if url.startswith('http://weibo.cn/'):
            pass
        elif url.startswith('weibo.cn/'):
            url = 'http://' + url
        else:
            raise ValueError('URL错误，请检查输入的URL是否为用户主页地址')
        if '?' in url:
            url = cut_line(url, '?')
    else:
        raise ValueError('URL错误，请检查输入的URL是否为用户主页地址')
    return url


def get_info(weibo_url):
    """get basic information of target user
    Args:
        weibo_url: target weibo user's homepage

    Returns:
        url_target, weibo_name, page_sum
    """
    url_target = weibo_url + '?filter=1&page=1'
    html = session.get(url_target, headers=HEADER).content
    target_info = etree.HTML(html)
    weibo_name = target_info.xpath('/html/head/title/text()')[0]  # get user name
    if weibo_name[-3:] == '的微博':
        weibo_name = weibo_name[:-3]
    elif weibo_name == '新浪通行证':  # stop in login page
        raise ConnectionError('Cookie可能已过期，请更新后再次尝试连接')
    elif weibo_name == '微博':
        raise ConnectionError('Cookie不能为空，请输入Cookie')
    elif weibo_name == '微博广场':
        raise ConnectionRefusedError('抱歉，你已被关进小黑屋，请等待数小时后再次尝试登陆')
    elif weibo_name == '我的首页':
        raise ReferenceError('请输入用户主页地址')
    else:
        raise SystemError('请检查目标用户主页地址和cookie')
    try:
        page_sum = target_info.xpath('//*[@id="pagelist"]/form/div/input[1]/@value')[0]  # get page sum
    except IndexError:
        page_sum = 1

    print_log('\nTarget: %s' % weibo_name)
    return url_target, weibo_name, page_sum


def make_directory(weibo_name):
    """make a directory named after weibo_name
    Args:
        weibo_name: weibo name of your target user
    """
    global folder_path
    folder_path = os.path.join(os.path.abspath('weibo'), weibo_name)
    try:
        try:
            os.mkdir(os.path.join(os.path.abspath('.'), 'weibo'))
        except FileExistsError:
            pass
        os.mkdir(folder_path)  # try to make a director
    except FileExistsError:
        pass


def get_date(post_info):
    """get the date when target post was sent
    Args:
        post_info: details about when target post was sent

    Returns:
        pic_date, pic_link, pic_series_name
    """
    if '月' in post_info[0:3]:  # 今年的微博  'xx月xx日 xx:xx 来自xxxx'
        post_date = time.strftime('%y-') + post_info.replace('月', '-').replace('日', '')[0:11]
    # FIXME: 一小时内的微博小概率产生一分钟的误差
    elif '前' in post_info[0:5]:  # 一小时内的微博  'xx分钟前 来自xxxx'
        post_info = cut_line(post_info, '分')
        minute = time.localtime()[4] - int(post_info)  # 现在22:05，45分钟前是负数  # type(post_info) = _ElementUnicodeResult
        if minute < 0:
            minute += 60
            hour = int(time.strftime('%H')) - 1
            post_date = time.strftime('%y-%m-%d ') + str(hour) + ':' + str(minute)
        else:
            post_date = time.strftime('%y-%m-%d %H:') + str(minute)
    elif '今天' in post_info[0:2]:  # 今天的微博  '今天 xx:xx 来自xxxx'
        post_date = time.strftime('%y-%m-%d ') + post_info[3:8]
    else:  # 今年之前的微博  'xxxx-xx-xx xx:xx:xx 来自xxxx'
        post_date = post_info[2:16]
    post_date_print = time.strptime(post_date, '%y-%m-%d %H:%M')
    post_date_print = time.strftime('%b %d %H:%M', post_date_print)
    return post_date, post_date_print


def traversal_weibo(url_target, weibo_name, page_sum):
    """traversal whole weibo
        Args:
            url_target: page to traversal
            page_sum: sum of pages
            weibo_name: weibo name of your target user
        """
    global page_counter

    for i in range(1, int(page_sum) + 1):  # search in all pages  range(1, int(page_sum) + 1)
        url = url_target.replace('page=1', 'page=%s' % i)
        html = session.get(url, headers=HEADER).content  # 获取页面源代码
        time.sleep(1)  # 等待页面加载
        target = etree.HTML(html)
        page_counter += 1
        for j in range(1, 11):  # by default each page have 10 posts
            try:
                post = target.xpath('//*[starts-with(@id, "M_")][%s]/div[1]/span[@class="ctt"]' % j)[0].xpath('string(.)')
                if '全文' in post[-2:]:
                    whole_post_url = 'http://weibo.cn/comment/' + target.xpath('//*[starts-with(@id, "M_")][%s]/@id' % j)[0][2:]
                    whole_post = session.get(whole_post_url, headers=HEADER).content
                    whole_post_tmp = etree.HTML(whole_post)
                    post = whole_post_tmp.xpath('//*[@id="M_"]/div[1]/span[@class="ctt"]')[0].xpath('string(.)')[1:]
            except IndexError:  # 到头了
                continue
            div_sum = target.xpath('//*[starts-with(@id, "M_")][%s]/div' % j)
            if len(div_sum) == 1:  # 没图的情况
                post_info = target.xpath('//*[starts-with(@id, "M_")][%s]/div[1]/span[@class="ct"]/text()' % j)[0]
            elif len(div_sum) == 2:  # 有图的情况
                post_info = target.xpath('//*[starts-with(@id, "M_")][%s]/div[2]/span[@class="ct"]/text()' % j)[0]

            post_date, post_date_print = get_date(post_info)
            print_log('\n%s               (page %s of %s)' % (post_info, i, page_sum))

            post_name = weibo_name + '_' + post_date
            make_pic(post, post_date_print, post_name, weibo_name)
        if page_counter % 10 == 0:
            timer(10)


def count_width(i, post):
    if FONT == 'NotoSansCJKsc-DemiLight.otf':
        width_one_one = ['105', '124']
        width_one_two = ['39', '44', '46', '58', '59', '73', '106', '108']
        width_one_three = ['33', '102']
        width_one_four = ['40', '41', '45', '91', '93', '123', '125']
        width_one_five = ['116']
        width_one_six = ['47', '92', '114']
        width_one_seven = ['34', '42', '63', '115']
        width_one_eight = ['120', '122']
        width_two = ['99']
        width_two_one = ['89', '118', '121']
        width_two_two = ['35', '36', '43', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57',
                         '60', '61', '62', '70', '74', '76', '94', '101', '107', '126']
        width_two_three = ['86', '88', '95', '97', '103', ]
        width_three = ['65', '69', '83', '84', '90', '96', '104', '110', '111', '117']
        width_three_one = ['67', '75', '80', '82', '98', '100', '112', '113']
        width_three_two = ['38', '66', '68', '71']
        width_three_three = ['72', '78', '79', '81', '85']
        width_four = ['77', '119']
        width_four_one = ['87']
        width_four_two = ['37', '64', '109']
        if str(ord(post[i])) in width_one_one:
            width = 0.52
        elif str(ord(post[i])) in width_one_two:
            width = 0.56
        elif str(ord(post[i])) in width_one_three:
            width = 0.65
        elif str(ord(post[i])) in width_one_four:
            width = 0.7
        elif str(ord(post[i])) in width_one_five:
            width = 0.75
        elif str(ord(post[i])) in width_one_six:
            width = 0.8
        elif str(ord(post[i])) in width_one_seven:
            width = 0.92
        elif str(ord(post[i])) in width_one_eight:
            width = 0.95
        elif str(ord(post[i])) in width_two:
            width = 1
        elif str(ord(post[i])) in width_two_one:
            width = 1.05
        elif str(ord(post[i])) in width_two_two:
            width = 1.1
        elif str(ord(post[i])) in width_two_three:
            width = 1.15
        elif str(ord(post[i])) in width_three:
            width = 1.2
        elif str(ord(post[i])) in width_three_one:
            width = 1.3
        elif str(ord(post[i])) in width_three_two:
            width = 1.4
        elif str(ord(post[i])) in width_three_three:
            width = 1.5
        elif str(ord(post[i])) in width_four:
            width = 1.65
        elif str(ord(post[i])) in width_four_one:
            width = 1.8
        elif str(ord(post[i])) in width_four_two:
            width = 1.9
        else:
            width = 2
    elif FONT == 'NotoSansCJKsc-Light.otf':
        width_one_one = ['39', '44', '46', '58', '59', '105', '106', '108', '124']
        width_one_two = ['73']
        width_one_three = ['33', '102']
        width_one_four = ['40', '41', '91', '93', '123', '125']
        width_one_five = ['45']
        width_one_six = ['114', '116']
        width_one_seven = ['47', '92']
        width_one_eight = ['34']
        width_one_nine = ['42', '63', '115', '120']
        width_one_ten = ['118', '122']
        width_two = ['89', '99', '121']
        width_two_one = ['74', '76', '107']
        width_two_two = ['35', '36', '43', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '60', '61',
                         '62', '70', '88', '94', '97', '101', '103', '126']
        width_two_three = ['86', '95']
        width_three = ['65', '69', '82', '83', '84', '90', '96', '98', '100', '104', '110', '111', '112', '113', '117']
        width_three_one = ['38', '66', '67', '75', '80']
        width_three_two = ['68', '71', '78', '85']
        width_three_three = ['72', '79', '81']
        width_four = ['77', '119']
        width_four_one = ['87']
        width_four_two = ['37', '64', '109']
        if str(ord(post[i])) in width_one_one:
            width = 0.52
        elif str(ord(post[i])) in width_one_two:
            width = 0.56
        elif str(ord(post[i])) in width_one_three:
            width = 0.6
        elif str(ord(post[i])) in width_one_four:
            width = 0.65
        elif str(ord(post[i])) in width_one_five:
            width = 0.7
        elif str(ord(post[i])) in width_one_six:
            width = 0.75
        elif str(ord(post[i])) in width_one_seven:
            width = 0.8
        elif str(ord(post[i])) in width_one_eight:
            width = 0.85
        elif str(ord(post[i])) in width_one_nine:
            width = 0.92
        elif str(ord(post[i])) in width_one_ten:
            width = 0.95
        elif str(ord(post[i])) in width_two:
            width = 1
        elif str(ord(post[i])) in width_two_one:
            width = 1.05
        elif str(ord(post[i])) in width_two_two:
            width = 1.1
        elif str(ord(post[i])) in width_two_three:
            width = 1.15
        elif str(ord(post[i])) in width_three:
            width = 1.2
        elif str(ord(post[i])) in width_three_one:
            width = 1.3
        elif str(ord(post[i])) in width_three_two:
            width = 1.4
        elif str(ord(post[i])) in width_three_three:
            width = 1.5
        elif str(ord(post[i])) in width_four:
            width = 1.6
        elif str(ord(post[i])) in width_four_one:
            width = 1.75
        elif str(ord(post[i])) in width_four_two:
            width = 1.9
        else:
            width = 2
    else:
        if 32 <= ord(post[i]) <= 126:
            width = 1
        else:
            width = 2
    return width


def change_line(post, i, formatted_post, width_counter, line_counter):
    if EASY_READ:
        # fixme 超长单词换行
        if (65 <= ord(post[i]) <= 90 or 97 <= ord(post[i]) <= 122) and post[i] != post[-1:]:  # 整个单词的话换行
            if 65 <= ord(post[i + 1]) <= 90 or 97 <= ord(post[i + 1]) <= 122:  #
                m = 1
                if 65 <= ord(post[i - m]) <= 90 or 97 <= ord(post[i - m]) <= 122:
                    while 65 <= ord(post[i - m]) <= 90 or 97 <= ord(post[i - m]) <= 122:
                        m += 1
                        if ord(post[i - m]) < 65 or 90 < ord(post[i - m]) < 97 or 122 < ord(post[i - m]):
                            formatted_post = formatted_post[:-m] + '\n' + formatted_post[-m:]
                            line_counter += 1
                            width_counter = 0
                            for n in range(i - m + 1, i + 1):
                                width_counter += count_width(n, post)
                            break
                elif post[i - m] == ' ':
                    formatted_post = formatted_post[:-m] + '\n' + formatted_post[-m:]
                    line_counter += 1
                    width_counter = count_width(i, post)
            else:
                formatted_post += '\n'
                line_counter += 1
                width_counter = 0
        else:
            formatted_post += '\n'
            line_counter += 1
            width_counter = 0
    else:
        formatted_post += '\n'
        line_counter += 1
        width_counter = 0
    return formatted_post, width_counter, line_counter


def format_post(post, formatted_post_date):
    width_counter = 0
    line_counter = 1
    formatted_post = ''
    for i in range(len(post)):
        if post[i] == ' ' and width_counter == 0:  # 去掉行首的空格
            pass
        elif post[i] in CH_PUN and width_counter == 0:  # 去掉行首的全角标点
            if post[i - 1] not in CH_PUN:
                formatted_post = formatted_post[:-2] + '\n' + formatted_post[-2:-1] + post[i]
                width_counter = count_width(i - 1, post) + count_width(i, post)
            elif post[i - 1] in CH_PUN or post[i + 1] in CH_PUN:
                formatted_post += post[i]
                width_counter = count_width(i, post)
        elif post[i] in EN_PUN and width_counter == 0:  # 去掉行首的半角标点
            if post[i - 1] in EN_PUN or post[i + 1] in EN_PUN:
                formatted_post += post[i]
                width_counter = count_width(i, post)
            else:
                formatted_post = formatted_post[:-1] + post[i] + '\n'
        elif post[i] == ' ' and i != (len(post) - 1):
            if FONT == 'NotoSansCJKsc-DemiLight.otf' or FONT == 'NotoSansCJKsc-Light.otf':
                if 32 <= ord(post[i - 1]) <= 126 or 32 <= ord(post[i + 1]) <= 126:
                    formatted_post += post[i] * 2
                    width_counter += 1.1
                else:
                    formatted_post += post[i] * 4
                    width_counter += 1.8
            else:
                if 32 <= ord(post[i - 1]) <= 126 or 32 <= ord(post[i + 1]) <= 126:
                    formatted_post += post[i]
                    width_counter += 1
                else:
                    formatted_post += post[i] * 2
                    width_counter += 2
        else:
            formatted_post += post[i]
            width_counter += count_width(i, post)
        if (int(width_counter) == 37 or int(width_counter) == 38) and i != (len(post) - 1):
            formatted_post, width_counter, line_counter = change_line(post, i, formatted_post, width_counter, line_counter)
    print_log(post, cout=False)
    print(formatted_post)
    return formatted_post, formatted_post_date, line_counter


def make_pic(post, formatted_post_date, post_name, weibo_name):
    global page_counter
    if os.path.isfile(os.path.join(os.path.abspath('weibo\\%s') % weibo_name, '\\%s.jpg' % post_name)):  # 这张微博已存在
        pass
        page_counter += 1
    else:  # 保存图片
        formatted_post, formatted_post_date, line_counter = format_post(post, formatted_post_date)
        layout(formatted_post, formatted_post_date, line_counter, post_name, weibo_name)


def layout(formatted_post, formatted_post_date, line_counter, post_name, weibo_name):
    if line_counter <= LAYOUT['line_sum']:
        width = 1080
        height = 1080
    else:
        width = 1080
        height = 1080 + (line_counter - LAYOUT['line_sum']) * LAYOUT['line_interval']
    image = Image.new('RGB', (width, height), COLOR_SCHEME['bg'])
    draw = ImageDraw.Draw(image)
    if LAYOUT == LAYOUT_ONE or LAYOUT == LAYOUT_TWO:
        font_date = ImageFont.truetype(os.path.join(os.path.abspath('font'), 'RobotoSlab-Thin.ttf'), LAYOUT['date_size'])
        font_post = ImageFont.truetype(os.path.join(os.path.abspath('font'), FONT), LAYOUT['post_size'])
        formatted_post_date = time.strptime(formatted_post_date, '%b %d %H:%M')
        formatted_post_date = time.strftime('%B %d %H:%M', formatted_post_date)
        formatted_post_date = formatted_post_date[:-9] + '\n' + formatted_post_date[-8:-6]
        if LAYOUT == LAYOUT_ONE:
            font_bg = ImageFont.truetype(os.path.join(os.path.abspath('font'), 'NotoSansCJKsc-DemiLight.otf'), 1080)
            draw.multiline_text((0, 0), '█\n' * int(line_counter / 12 + 1), font=font_bg, fill=COLOR_SCHEME['text'], spacing=-173)
        draw.multiline_text(LAYOUT['date_site'], formatted_post_date, font=font_date, fill=COLOR_SCHEME['text'], spacing=LAYOUT['date_spacing'])
        if LAYOUT == LAYOUT_ONE:
            draw.multiline_text(LAYOUT['text_site'], formatted_post, font=font_post, fill=COLOR_SCHEME['text'], spacing=LAYOUT['post_spacing'])
        elif LAYOUT == LAYOUT_TWO:
            draw.multiline_text(LAYOUT['text_site'], formatted_post, font=font_post, fill=COLOR_SCHEME['bg'], spacing=LAYOUT['post_spacing'])
    elif LAYOUT == LAYOUT_THREE:
        font_date = ImageFont.truetype(os.path.join(os.path.abspath('font'), FONT), LAYOUT['date_size'])
        font_post = ImageFont.truetype(os.path.join(os.path.abspath('font'), FONT), LAYOUT['post_size'])
        draw.text(LAYOUT['date_site'], formatted_post_date, font=font_date, fill=COLOR_SCHEME['text'])
        draw.multiline_text(LAYOUT['text_site'], formatted_post, font=font_post, fill=COLOR_SCHEME['text'], spacing=LAYOUT['post_spacing'])
    # image.show()
    post_name = post_name.replace('-', '').replace(':', '').replace(' ', '_')  # 文件名不能包含:
    image.save(os.path.join(os.path.abspath('weibo'), weibo_name) + '\\%s.jpg' % post_name, 'jpeg')


def main():
    start_time = time.time()
    print_log('\n' * 5, '=' * 30, time.strftime('%Y-%m-%d %H:%M:%S'), '=' * 30, cout=False)
    print_log('\nWeibo Carrier')
    try:
        print_log('\nLink start...')
        for weibo_url in URL[:]:
            weibo_url = url_interpreter(weibo_url)
            url_target, weibo_name, page_sum = get_info(weibo_url)
            make_directory(weibo_name)
            traversal_weibo(url_target, weibo_name, page_sum)
    except ConnectionRefusedError:
        print_log('\n抱歉，你已被关进小黑屋，请等待数小时后再次尝试登陆')
    except TimeoutError:
        print_log('\n由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败')
    except KeyboardInterrupt:
        print_log('\nKeyboard Interrupt')
    except Exception as e:
        print_log('\nError: ', str(e), '\n请重新尝试连接')
    finally:
        time_cost = int(time.time() - start_time)
        print_log('\nCost %d min %d sec' % (time_cost // 60, time_cost % 60))

#  FIXME: emoji
#  FIXME: 颜文字
if __name__ == '__main__':
    main()
