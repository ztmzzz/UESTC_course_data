import logging
import time
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.keys import Keys
from path import *

# 该文件为改进版本，能够并行运行
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
# for循环schoolId 自己修改list1中的值
for schoolId in range(30, 3500):
    # schoolId = 662
    url = "https://gkcx.eol.cn/school/" + str(schoolId)
    driver.get(url)
    with open('done.txt', 'r', encoding='utf-8') as f:
        done = f.readlines()
        if str(schoolId)+'\n' in done:
            continue
    try:
        ben = driver.find_element_by_xpath(
            '//*[@id="root"]/div/div[1]/div/div/div/div[1]/div[2]/div/div/div[3]/div[2]/div[3]/div[1]')
        if ben.text == '普通本科':
            url = url + "/provinceline"
            driver.get(url)
            with open('done.txt', 'a+', encoding='utf-8') as f:
                f.write(str(schoolId) + '\n')
        else:
            continue
    except:
        continue
    # sleep(3)
    # 恢复标志符
    resume = False
    # for i in ["provinceScore", "plane", "subjectScore"]:  # 对于三个表格遍历

    for i in ["provinceScore", "plane", "subjectScore"]:  # 恢复时使用
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
            gotoState(i, "新疆")
            nowProvince = "新疆"
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
                                        writeData(data, i + ".txt", dict[i], nowProvince, nowYear, nowWenli, nowBatch,
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
                                    writeData(data, i + ".txt", dict[i], nowProvince, nowYear, nowWenli, nowBatch, "",
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
                            writeData(data, i + ".txt", dict[i], nowProvince, nowYear, nowWenli, "", "", school, True)
                        else:
                            writeData(data, i + ".txt", dict[i], nowProvince, nowYear, nowWenli, "", "", school, False)
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
