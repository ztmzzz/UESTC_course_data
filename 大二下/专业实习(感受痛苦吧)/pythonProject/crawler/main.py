import logging
import time
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from path import *

# 该文件为初始版本，能够根据list的值爬取数据
# 根据电脑速度调整sleep的值，如果遇到错误就从这个省份重新开始爬取，带有错误恢复的地方是需要修改的地方

def nextAction(path):
    try:
        e = driver.find_element_by_xpath(path)
        e.click()
        sleep(0.2)
        e.send_keys(Keys.DOWN)
        e.send_keys(Keys.ENTER)
        sleep(0.4)
    except:
        file_name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # driver.save_screenshot(file_name)
        driver.get_screenshot_as_file(file_name)
        raise


# 设置下一项
def setNext(name, type):
    a = -1
    try:
        if type == "province":
            a = 0
        elif type == "year":
            a = 1
        elif type == "wenli":
            a = 2
        elif type == "batch":
            a = 3
        elif type == "special":
            a = 4
        else:
            logging.log(logging.WARNING, "选择的类别错误，如年份")
        if name == "provinceScore":
            nextAction(provinceScoreXpath[a])
        elif name == "plane":
            nextAction(planeXpath[a])
        elif name == "subjectScore":
            if type == "year":
                try:
                    e = driver.find_elements_by_css_selector("#form3 > div > div > div > span > div > div")
                    e = e[1]
                    e.click()
                    sleep(0.2)
                    e.send_keys(Keys.DOWN)
                    e.send_keys(Keys.ENTER)
                    sleep(0.5)
                except:
                    file_name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    # driver.save_screenshot(file_name)
                    driver.get_screenshot_as_file(file_name)
                    raise
            else:
                nextAction(subjectScoreXpath[a])
        else:
            logging.log(logging.WARNING, "选择的区域错误，如各省分数线")
    except:
        file_name = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # driver.save_screenshot(file_name)
        driver.get_screenshot_as_file(file_name)
        raise


# 获取数据，同时防止反爬
def getData(path):
    try:
        data = driver.find_element_by_xpath(path)
    except StaleElementReferenceException:
        logging.log(logging.WARNING, "读取出错")
        sleep(10)
        data = driver.find_element_by_xpath(path)

    trContent = data.find_elements_by_tag_name('tr')
    dat = []
    lst = []
    for i in range(len(trContent)):
        for td in trContent[i].find_elements_by_tag_name('td'):
            if td.text != '':
                lst.append(td.text)
        dat.append(lst)
        lst = []
    return dat


def isElementExist(path):
    try:
        driver.find_element_by_xpath(path)
        return True
    except:
        return False


# 按照格式写入文本文档
def writeData(data, path, type, province, year, wenli, batch, special, school, isSpecail):
    with open(path, 'a+', encoding='utf-8') as f:
        data = data[1:]
        for i in data:
            t = []
            for tmp in i:
                if (tmp == "-") | (tmp == "-/-"):
                    t.append(" ")
                else:
                    t.append(tmp)
            i = t
            temp = school + '\t' + province + '\t' + str(year) + '\t' + wenli
            if type == 0:
                if i[3] == ' ':
                    a = [" ", " "]
                else:
                    a = i[3].split("/")
                temp = temp + '\t' + i[1] + '\t' + i[2] + '\t' + a[0] + '\t' + a[1] + '\t' + i[4]
                if isSpecail:
                    temp = temp + '\t' + i[-1]
                else:
                    temp = temp + '\t' + " "
            elif type == 1:
                temp = temp + '\t' + batch + '\t' + i[0] + '\t' + i[1] + '\t' + i[2] + '\t' + i[3]
                if isSpecail:
                    temp = temp + '\t' + special + '\t' + i[4]
                else:
                    temp = temp + '\t' + " " + '\t' + " "
            elif type == 2:
                if i[3] == ' ':
                    a = [" ", " "]
                else:
                    a = i[3].split("/")
                temp = temp + '\t' + batch + '\t' + i[0] + '\t' + i[2] + '\t' + a[0] + '\t' + a[1]
                if isSpecail:
                    temp = temp + '\t' + special + '\t' + i[4]
                else:
                    temp = temp + '\t' + " " + '\t' + " "
            temp = temp.replace("-", " ")
            f.write(temp + '\n')  # 加\n换行显示


# 出错时恢复使用
def gotoState(name, province):
    nowProvince = driver.find_element_by_xpath(eval(name + "Xpath[0]")).text
    while nowProvince != province:
        setNext(name, "province")
        nowProvince = driver.find_element_by_xpath(eval(name + "Xpath[0]")).text


option = webdriver.ChromeOptions()
option.add_argument('--disable-gpu')
option.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                    '537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"')
driver = webdriver.Chrome("./chromedriver.exe")
list1 = ['96', '97', '98', '99', '100', '101', '102',
         '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118',
         '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134',
         '135', '136', '137', '138', '139', '140', '142', '143', '144', '146', '147', '148', '149', '150', '151', '152',
         '153', '154', '156', '157', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167', '168', '169',
         '170', '171', '172', '173', '174', '175', '176', '177', '178', '179', '180', '182', '183', '184', '185', '186',
         '187', '188', '189', '190', '191', '192', '193', '194', '195', '196', '197', '198', '199', '200', '201', '202',
         '203', '204', '205', '206', '207', '208', '209', '210', '211', '212', '213', '214', '215', '216', '217', '218',
         '219', '220', '221', '222', '223', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233', '234',
         '235', '236', '237', '238', '239', '240', '241', '242', '243', '244', '245', '246', '247', '248', '249', '250',
         '251', '252', '253', '254', '255', '256', '257', '258', '259', '260', '262', '263', '264', '265', '266', '267',
         '268', '269', '270', '271', '272', '273', '274', '275', '276', '277', '278', '279', '280', '281', '282', '283',
         '284', '285', '286', '287', '288', '289', '290', '291', '292', '293', '294', '295', '296', '297', '298', '299',
         '300', '301', '302', '303', '304', '305', '306', '307', '308', '309', '310', '311', '312', '313', '314', '315',
         '316', '317', '318', '320', '322', '323', '324', '325', '326', '327', '328', '329', '330', '331', '332', '333',
         '334', '335', '336', '337', '338', '339', '340', '341', '342', '343', '344', '345', '346', '347', '348', '349',
         '350', '351', '352', '353', '354', '355', '356', '357', '358', '359', '360', '361', '362', '363', '364', '365',
         '366', '367', '368', '369', '370', '371', '372', '373', '374', '375', '376', '377', '378', '379', '380', '381',
         '382', '383', '384', '385', '386', '387', '388', '389', '390', '391', '392', '393', '394', '395', '396', '397',
         '398', '399', '400', '401', '402', '403', '404', '405', '406', '407', '408', '409', '410', '411', '412', '413',
         '414', '415', '416', '417', '418', '419', '420', '421', '422', '423', '424', '425', '426', '427', '428', '429',
         '430', '431', '432', '433', '434', '435', '436', '437', '438', '439', '440', '441', '442', '443', '444', '445',
         '446', '447', '448', '449', '450', '451', '452', '453', '454', '455', '456', '457', '458', '459', '460', '461',
         '462', '463', '464', '465', '466', '468', '469', '470', '471', '472', '473', '474', '475', '476', '477', '478',
         '479', '480', '481', '482', '483', '484', '485', '487', '488', '489', '490', '491', '492', '493', '494', '495',
         '496', '498', '499', '500', '501', '502', '504', '505', '506', '507', '508', '509', '510', '511', '512', '514',
         '515', '516', '517', '518', '519', '520', '521', '522', '523', '525', '526', '527', '528', '529', '530', '531',
         '532', '533', '534', '535', '536', '537', '538', '539', '540', '541', '542', '543', '544', '545', '546', '547',
         '548', '549', '550', '551', '552', '553', '554', '555', '556', '557', '558', '559', '561', '562', '563', '564',
         '565', '566', '567', '568', '569', '570', '571', '572', '573', '574', '575', '576', '578', '579', '580', '581',
         '583', '584', '585', '586', '587', '589', '590', '591', '592', '594', '595', '596', '597', '598', '599', '600',
         '601', '602']
# for循环schoolId 自己修改list1中的值
for schoolId in list1:
    schoolId = 935
    url = "https://gkcx.eol.cn/school/" + str(schoolId) + "/provinceline"
    driver.get(url)
    # sleep(5)
    # 恢复标志符
    resume = True
    # for i in ["provinceScore", "plane", "subjectScore"]:  # 对于三个表格遍历
    for i in ["subjectScore"]:  # 恢复时使用
        school = driver.find_element_by_xpath(schoolXpath).text
        dict = {"provinceScore": 0, "plane": 1, "subjectScore": 2}
        setNext(i, "province")
        e = driver.find_element_by_xpath(eval(i + "Xpath[0]"))
        e.click()
        sleep(0.2)
        e.send_keys(Keys.UP)
        e.send_keys(Keys.ENTER)
        sleep(0.4)
        startProvince = driver.find_element_by_xpath(eval(i + "Xpath[0]")).text
        nowProvince = startProvince
        # 恢复用
        if resume:
            gotoState(i, "河南")
            nowProvince = "河南"
            resume = False
        while True:  # 省份遍历
            if i == "subjectScore":
                e = driver.find_elements_by_css_selector("#form3 > div > div > div > span > div > div")
                startYear = e[1].text
            else:
                startYear = driver.find_element_by_xpath(eval(i + "Xpath[1]")).text
            nowYear = startYear
            while True:  # 年份遍历
                startWenli = driver.find_element_by_xpath(eval(i + "Xpath[2]")).text
                nowWenli = startWenli
                while True:  # 文理科遍历
                    if i != "provinceScore":
                        startBatch = driver.find_element_by_xpath(eval(i + "Xpath[3]")).text
                        nowBatch = startBatch
                        while True:  # 批次遍历
                            if (nowProvince in ["北京", "天津", "上海", "江苏", "福建", "湖北", "湖南", "广东", "海南"]) & (
                                    isElementExist(eval(i + "Xpath[4]"))):
                                startSpecial = driver.find_element_by_xpath(eval(i + "Xpath[4]")).text
                                nowSpecial = startSpecial
                                while True:  # 专业组遍历
                                    while True:  # 处理多页
                                        try:
                                            data = getData(bodyXpath[dict[i]])
                                        except:
                                            sleep(2)
                                            data = getData(bodyXpath[dict[i]])
                                        writeData(data, i + "211.txt", dict[i], nowProvince, nowYear, nowWenli, nowBatch,
                                                  nowSpecial, school, True)
                                        if isElementExist(nextButtonXpath[dict[i]]):
                                            button = driver.find_element_by_xpath(nextButtonXpath[dict[i]])
                                            if button.get_attribute('aria-disabled') == "False":
                                                button.click()
                                                sleep(1)
                                            else:
                                                break
                                        else:
                                            break
                                    setNext(i, "special")
                                    nowSpecial = driver.find_element_by_xpath(eval(i + "Xpath[4]")).text
                                    if nowSpecial == startSpecial:
                                        break
                            else:
                                while True:  # 处理多页
                                    try:
                                        data = getData(bodyXpath[dict[i]])
                                    except:
                                        sleep(2)
                                        data = getData(bodyXpath[dict[i]])
                                    writeData(data, i + "211.txt", dict[i], nowProvince, nowYear, nowWenli, nowBatch, "",
                                              school,
                                              False)
                                    if isElementExist(nextButtonXpath[dict[i]]):
                                        button = driver.find_element_by_xpath(nextButtonXpath[dict[i]])
                                        if (button.get_attribute('aria-disabled') == "false") | (
                                                button.get_attribute('aria-disabled') == "False"):
                                            button.click()
                                            sleep(1)
                                        else:
                                            break
                                    else:
                                        break
                            setNext(i, "batch")
                            nowBatch = driver.find_element_by_xpath(eval(i + "Xpath[3]")).text
                            if nowBatch == startBatch:
                                break
                    else:
                        try:
                            data = getData(bodyXpath[dict[i]])
                        except:
                            sleep(2)
                            data = getData(bodyXpath[dict[i]])
                        if nowProvince in ["北京", "天津", "上海", "江苏", "福建", "湖北", "湖南", "广东", "海南"]:
                            writeData(data, i + "211.txt", dict[i], nowProvince, nowYear, nowWenli, "", "", school, True)
                        else:
                            writeData(data, i + "211.txt", dict[i], nowProvince, nowYear, nowWenli, "", "", school, False)
                    setNext(i, "wenli")
                    nowWenli = driver.find_element_by_xpath(eval(i + "Xpath[2]")).text
                    if nowWenli == startWenli:
                        break
                setNext(i, "year")
                if i == "subjectScore":
                    e = driver.find_elements_by_css_selector("#form3 > div > div > div > span > div > div")
                    nowYear = e[1].text
                else:
                    nowYear = driver.find_element_by_xpath(eval(i + "Xpath[1]")).text
                if nowYear == startYear:
                    break
            setNext(i, "province")
            nowProvince = driver.find_element_by_xpath(eval(i + "Xpath[0]")).text
            if nowProvince == startProvince:
                break
