# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------
''''''
import hashlib
import time
import os
import traceback
import re
import random
import base64
import html as html_decode
from colorama import Fore
from tqdm import tqdm as td

import xlrd
import xlwt
from lxml import etree
from xlutils.copy import copy
from requests_html import HTMLSession

Session = HTMLSession()
"""
爬虫请求模块，HTMLSession提供了Xpath方法，方便直接进行解析
Crawler request module, HTMLSession provides Xpath method, convenient for parsing directly

for example,
response = jrbox.Session.get(url, headers, cookies, params)
for div in response.html.xpath('.//div'):
    title = div.xpath('*******')
:return: requests_html.HTMLSession的实例化方法
"""


def test():
    print('hello world!')
    print(Fore.YELLOW + '人生苦短，我用Python！')
    print(Fore.LIGHTWHITE_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTRED_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTMAGENTA_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTGREEN_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTCYAN_EX + '人生苦短，我用Python！')
    print(Fore.LIGHTBLUE_EX + '人生苦短，我用Python！')
    print(Fore.CYAN + '人生苦短，我用Python！')
    print(Fore.LIGHTYELLOW_EX + '人生苦短，我用Python！')
    print(Fore.RED + '人生苦短，我用Python！')
    print(Fore.BLUE + '人生苦短，我用Python！')
    print(Fore.GREEN + '人生苦短，我用Python！')
    print(Fore.MAGENTA + '人生苦短，我用Python！')
    print(Fore.RESET + '人生苦短，我用Python！')


def md5value(data):
    input_name = hashlib.md5()
    input_name.update(data.encode("utf-8"))
    # print("大写的32位" + (input_name.hexdigest()).upper())
    # print("大写的16位" + (input_name.hexdigest())[8:-8].upper())
    # print("小写的32位" + (input_name.hexdigest()).lower())
    # print("小写的16位" + (input_name.hexdigest())[8:-8].lower())
    token = ((input_name.hexdigest()).upper(),
             (input_name.hexdigest())[8:-8].upper(),
             (input_name.hexdigest()).lower(),
             (input_name.hexdigest())[8:-8].lower(),
             )
    return token


def to_stamp(format_time):
    """
    2016-05-05 20:28:54 ----> 10位时间戳
    :param format_time:
    :return:
    """
    time_tuple = time.strptime(format_time, "%Y-%m-%d %H:%M:%S")
    timestamp = str(int(time.mktime(time_tuple)))
    # print(timestamp)
    return timestamp


def to_date(start):
    """
    start = ['567100800', '1632844924200'] --->支持10位，13位时间戳转标准时间
    start = '2022-09-06 00:15:01' ---> 支持标准时间转10位时间戳
    :param start:
    :return:
    """
    starttime = []
    if type(start) == list:
        for timestamp in start:
            timestamp = list(timestamp)
            timestamp = int(''.join(timestamp[0: 10:]))
            time_local = time.localtime(timestamp)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            starttime.append(dt)
        return starttime
    if type(start) == str:
        timestamp = list(start)
        timestamp = int(''.join(timestamp[0: 10:]))
        time_local = time.localtime(timestamp)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        return dt


def SaveExcel(filename, data, Excel_head):
    """
    file_name = '测试数据'
    a = 'hello'
    b = 'world'
    c = '!'
    data = {
        file_name: [[a], [b], [c]]
    }
    print(data)
    Excel_head = ('你好', '世界', '!!!')
    ku.SaveExcel(file_name, data, Excel_head)

    :param data: Type == dict       -->
    :param filename: Type == str
    :param Excel_head: Type == tuple
    :return: None
    """
    try:
        # 创建保存excel表格的文件夹
        # os.getcwd() 获取当前文件路径
        os_mkdir_path = os.getcwd() + '/数据/'
        # 判断这个路径是否存在，不存在就创建
        if not os.path.exists(os_mkdir_path):
            os.mkdir(os_mkdir_path)
        # 判断excel表格是否存在           工作簿文件名称
        os_excel_path = os_mkdir_path + f'{filename}.xls'

        if not os.path.exists(os_excel_path):
            # 不存在，创建工作簿(也就是创建excel表格)
            workbook = xlwt.Workbook(encoding='utf-8')
            """工作簿中创建新的sheet表"""  # 设置表名
            worksheet1 = workbook.add_sheet(filename, cell_overwrite_ok=True)
            """设置sheet表的表头"""
            sheet1_headers = Excel_head
            # 将表头写入工作簿
            for header_num in range(0, len(sheet1_headers)):
                # 设置表格长度
                worksheet1.col(header_num).width = 2560 * 3
                # 写入            行, 列,           内容
                worksheet1.write(0, header_num, sheet1_headers[header_num])
            # 循环结束，代表表头写入完成，保存工作簿
            workbook.save(os_excel_path)
        # 判断工作簿是否存在
        if os.path.exists(os_excel_path):
            # 打开工作簿
            workbook = xlrd.open_workbook(os_excel_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # 获取工作薄中所有表中的表名与数据名对比
                    if worksheet.name == name:
                        # 获取表中已存在的行数
                        rows_old = worksheet.nrows
                        # 将xlrd对象拷贝转化为xlwt对象
                        new_workbook = copy(workbook)
                        # 获取转化后的工作薄中的第i张表
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_excel_path)
    except:
        traceback.print_exc()
        print('异常:', data)


html_clean = lambda text: re.sub(r'<[^>]+>', '', text)
"""
传入文本  -->  输出清除HTML标签后的文本
:param text: Type == str
:return: new text
"""

filename_clean = lambda filename: re.sub(r"[\/\\\:\*\?\"\<\>\|]", "_", filename)
"""
传入文本 --> 输出清除文件名非法字符后的文本
:param filename: Type == str
:return: new name
"""


def SaveExcels(file_name, data, sheet, Excel_head):
    """
file_name = '测试一下了'
Excel_head = ('你', '好', '世', '界', '!')
for i in range(1, 3):
    sheet = f'第{i}页' # 生成每一页的表名
    data = {
        sheet: ['h', 'e', 'l', 'l', 'o']   # [str, str, str, str, str]
    }
    print(data)
    ku.SaveExcels(file_name, data, sheet, Excel_head)


    :param file_name: Type == str
    :param data: Type == dict
    :param sheet: Type == str
    :param Excel_head: Type == tuple
    :return: None
    """
    try:
        # 获取表的名称
        sheet_name = [i for i in data.keys()][0]
        # 创建保存excel表格的文件夹
        # os.getcwd() 获取当前文件路径
        os_mkdir_path = os.getcwd() + '/数据/'
        # 判断这个路径是否存在，不存在就创建
        if not os.path.exists(os_mkdir_path):
            os.mkdir(os_mkdir_path)
        # 判断excel表格是否存在           工作簿文件名称
        os_excel_path = os_mkdir_path + f'{file_name}.xls'
        if not os.path.exists(os_excel_path):
            # 不存在，创建工作簿(也就是创建excel表格)
            workbook = xlwt.Workbook(encoding='utf-8')
            """工作簿中创建新的sheet表"""  # 设置表名
            worksheet1 = workbook.add_sheet(sheet, cell_overwrite_ok=True)
            """设置sheet表的表头"""
            sheet1_headers = Excel_head
            # 将表头写入工作簿
            for header_num in range(0, len(sheet1_headers)):
                # 设置表格长度
                worksheet1.col(header_num).width = 2560 * 3
                # 写入表头        行,    列,           内容
                worksheet1.write(0, header_num, sheet1_headers[header_num])
            # 循环结束，代表表头写入完成，保存工作簿
            workbook.save(os_excel_path)
        """=============================已有工作簿添加新表==============================================="""
        # 打开工作薄
        workbook = xlrd.open_workbook(os_excel_path)
        # 获取工作薄中所有表的名称
        sheets_list = workbook.sheet_names()
        # 如果表名称：字典的key值不在工作簿的表名列表中
        if sheet_name not in sheets_list:
            # 复制先有工作簿对象
            work = copy(workbook)
            # 通过复制过来的工作簿对象，创建新表  -- 保留原有表结构
            sh = work.add_sheet(sheet_name)
            # 给新表设置表头
            excel_headers_tuple = Excel_head
            for head_num in range(0, len(excel_headers_tuple)):
                sh.col(head_num).width = 2560 * 3
                #               行，列，  内容，            样式
                sh.write(0, head_num, excel_headers_tuple[head_num])
            work.save(os_excel_path)
        """========================================================================================="""
        # 判断工作簿是否存在
        if os.path.exists(os_excel_path):
            # 打开工作簿
            workbook = xlrd.open_workbook(os_excel_path)
            # 获取工作薄中所有表的个数
            sheets = workbook.sheet_names()
            for i in range(len(sheets)):
                for name in data.keys():
                    worksheet = workbook.sheet_by_name(sheets[i])
                    # 获取工作薄中所有表中的表名与数据名对比
                    if worksheet.name == name:
                        # 获取表中已存在的行数
                        rows_old = worksheet.nrows
                        # 将xlrd对象拷贝转化为xlwt对象
                        new_workbook = copy(workbook)
                        # 获取转化后的工作薄中的第i张表
                        new_worksheet = new_workbook.get_sheet(i)
                        for num in range(0, len(data[name])):
                            new_worksheet.write(rows_old, num, data[name][num])
                        new_workbook.save(os_excel_path)
    except Exception:
        traceback.print_exc()
        print('异常：', data)


def ip_to_address(ip):
    """

    :param ip: Type == str
    :return: Type == str
    """
    params = (
        ('query', ip),
        ('co', ''),
        ('resource_id', '5809'),
        ('t', '1661598345836'),
        ('ie', 'utf8'),
        ('oe', 'gbk'),
        ('cb', ['op_aladdin_callback', 'jQuery110206508062660667266_1661598209405']),
        ('format', 'json'),
        ('tn', 'baidu'),
        ('_', '1661598209414'),
    )
    response = Session().get('https://sp1.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php', params=params).text
    location = re.findall('"location":"(.*?)"', response, re.S)[0]
    address = location.encode('utf-8').decode('unicode-escape')
    return address


def Fanyi(keyword, From, To):
    """
    I have upgraded Youdao Translation to support multi-language translation,
    not just translation between Chinese and foreign languages.
    For example,

    result = Fanyi('hello', '英', '小日本')
    print(result)
    ==============================================================================================
    countries_dict
    dic = {
        '中': 'zh-CHS', '英': 'en', '日': 'ja', '小鬼子': 'ja', '小日本': 'ja', '日本省': 'ja', '韩': 'ko', '法': 'fr',
        '德': 'de', '俄': 'ru', '西班牙': 'es', '葡萄牙': 'pt', '意大利': 'it', '越南': 'vi', '印尼': 'id', '阿拉伯': 'ar',
        '荷兰': 'nl', '泰': 'tb'
    }
    ==============================================================================================
    :param keyword: Type == str
    :param From: Type == str
    :param To: Type == str
    :return: Type == str
    """
    url = 'https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://fanyi.youdao.com',
        'Referer': 'https://fanyi.youdao.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    cookies = "OUTFOX_SEARCH_USER_ID=1232339712@10.169.0.102; OUTFOX_SEARCH_USER_ID_NCOO=1448598951.7804058; fanyi-ad-id=305838; fanyi-ad-closed=1; YOUDAO_FANYI_SELECTOR=ON; ___rl__test__cookies=1654410123235"
    cookies_dict = {}
    for i in cookies.split('; '):
        cookies_dict[i.split('=')[0]] = i.split('=')[1]

    dic = {
        '中': 'zh-CHS', '英': 'en', '日': 'ja', '小鬼子': 'ja', '小日本': 'ja', '日本省': 'ja', '韩': 'ko', '法': 'fr',
        '德': 'de', '俄': 'ru', '西班牙': 'es', '葡萄牙': 'pt', '意大利': 'it', '越南': 'vi', '印尼': 'id', '阿拉伯': 'ar',
        '荷兰': 'nl', '泰': 'tb'
    }
    if '中' in [From, To]:
        lts = str(int(time.time() * 1000))
        salt = "" + str(int(time.time() * 1000)) + str(random.randint(1, 10))
        str_ = "fanyideskweb" + keyword + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        sign = md5value(str_)[2]

        data = {
            'i': keyword,
            'from': dic[From],
            'to': dic[To],
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'lts': lts,
            'bv': '85618492e851e16ca0a03b8e100fdddb',
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION'
        }
        try:
            response = Session().post(url=url, headers=headers, data=data,
                                      cookies=cookies_dict).json()["translateResult"][0][0]["tgt"]
            return response
            # print('翻译结果为:', response["translateResult"][0][0]["tgt"])

        except:
            text = '翻译失败'
            return text


    else:
        try:
            lts = str(int(time.time() * 1000))
            salt = "" + str(int(time.time() * 1000)) + str(random.randint(1, 10))
            str_ = "fanyideskweb" + keyword + salt + "Ygy_4c=r#e#4EX^NUGUc5"
            sign = md5value(str_)[2]
            data = {
                'i': keyword,
                'from': dic[From],
                'to': dic['中'],
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': salt,
                'sign': sign,
                'lts': lts,
                'bv': '85618492e851e16ca0a03b8e100fdddb',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_CLICKBUTTION'
            }

            response = Session().post(url=url, headers=headers, data=data,
                                      cookies=cookies_dict).json()
            keyword = response["translateResult"][0][0]["tgt"]

            lts = str(int(time.time() * 1000))
            salt = "" + str(int(time.time() * 1000)) + str(random.randint(1, 10))
            str_ = "fanyideskweb" + keyword + salt + "Ygy_4c=r#e#4EX^NUGUc5"
            sign = md5value(str_)[2]
            data = {
                'i': keyword,
                'from': dic['中'],
                'to': dic[To],
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': salt,
                'sign': sign,
                'lts': lts,
                'bv': '85618492e851e16ca0a03b8e100fdddb',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_CLICKBUTTION'
            }

            response = Session().post(url=url, headers=headers, data=data,
                                      cookies=cookies_dict).json()["translateResult"][0][0]["tgt"]
            # print('翻译结果为:', response["translateResult"][0][0]["tgt"])
            return response
        except:
            text = '翻译失败'
            return text


text_to_base64 = lambda text: base64.b64encode(text.encode('utf-8')).decode("utf-8")
"""
:param text: Type == str
:return: Type == str
"""

base64_to_text = lambda text: base64.b64decode(text.encode("utf-8")).decode("utf-8")
"""
:param text: Type == str
:return: Type == str
"""


def mkdir(dir_name):
    """
    If yes, print the path.
    If no, create a subfolder in the current directory.
    :param dir_name: Type == str
    :return: None
    """
    os_mkdir_path = os.getcwd() + f'/{dir_name}/'
    # 判断这个路径是否存在，不存在就创建
    if not os.path.exists(os_mkdir_path):
        os.mkdir(os_mkdir_path)
        print('=================路径不存在，已进行创建==================')
    else:
        print(f'路径存在:{os_mkdir_path}')


video_pojie = lambda url: 'http://okjx.cc/?url=' + url
"""
支持众多主流视频站点:API拼接网页链接，访问即可
:param url: Type == str
:return: Type == str
"""

html_node_text = lambda HTML, XPATH: html_decode.unescape(
    html_clean(str(etree.tostring(etree.HTML(HTML).xpath(XPATH)[0])))).lstrip("b'").rstrip("'")
"""
单节点方法，xpath列表请调用html_nodes_text方法
HTML: Web site source code
XPATH: Node XPATH Syntax
retur: Node, the front page display text data
"""


def html_nodes_text(XPATH_list):
    """
    :param XPATH_list: Type == list 传入Xpath匹配到的节点群
    :return: Type == list 返回清洗后HTML标签后的文本
    """
    text_list = []
    for Xpath in XPATH_list:
        result = html_decode.unescape(html_clean(str(etree.tostring(Xpath)))).lstrip("b'").rstrip("'")
        text_list.append(result)
    return text_list


def console(self, *args, sep=' ', end='\n', file=None, color=None, model=True):
    """
    :param self:
    :param args:
    :param sep:
    :param end:
    :param file:
    :param color: if model == True --> color = '黄色'
                  if model == False --> color = 'Fore.YELLOW'
    :return:
    """
    dic = {
        '黄色': 'Fore.YELLOW', '+黄色': 'Fore.LIGHTYELLOW_EX',
        '红色': 'Fore.RED', '+红色': 'Fore.LIGHTRED_EX',
        '青色': 'Fore.CYAN', '+青色': 'Fore.LIGHTCYAN_EX',
        '绿色': 'Fore.GREEN', '+绿色': 'Fore.LIGHTGREEN_EX',
        '蓝色': 'Fore.BLUE', '+蓝色': 'Fore.LIGHTBLUE_EX',
        '黑色': 'Fore.BLACK', '+黑色': 'Fore.LIGHTBLACK_EX',
        '品红色': 'Fore.MAGENTA', '+白色': 'Fore.LIGHTWHITE_EX'
    }
    if color != None:
        if model != False:
            color = eval(dic[color])
        else:
            color = eval(color)
    else:
        color = Fore.LIGHTYELLOW_EX
    print(color + str(self), *args, sep=sep, end=end, file=file)

tqdm = td
