from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from lxml import etree

from query_school import Client
from save_data import ToSql


class Crawler(object):
    def __init__(self):
        self.first_url = "https://gkcx.eol.cn/school/39/specialtyline?cid=0"
        self.base_url = "https://gkcx.eol.cn/school/%s/specialtyline?cid=0"
        self.opt = webdriver.ChromeOptions()
        # self.opt.add_argument("--headless")
        # self.opt.add_argument("--no-sandbox")
        self.driver = webdriver.Chrome(options=self.opt, executable_path="/usr/local/bin/chromedriver")
        self.wait = WebDriverWait(self.driver, 5)
        self.mysql = ToSql()

    def page_down(self):
        """
        向下翻页
        :return:
        """
        try:
            if self.driver.find_element_by_xpath("//li[text()='1']").get_attribute("class") == "none":
                start = 0
            else:
                start = 1
            pages = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fypages']/ul/li[@class]")))
            for page_num in range(start, len(pages)):
                pages = self.wait.until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fypages']/ul/li[@class]")))
                pages[page_num].click()
                time.sleep(1)
                self.get_data()
            pages = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='fypages']/ul/li[@class]")))
            pages[0].click()
            time.sleep(0.5)

        except (TimeoutException, IndexError, NoSuchElementException):
            pass

    @staticmethod
    def get_search_word(major_name):
        """
        通过major_name处理，获取search_name
        :param major_name:
        :return:
        """
        search_word = major_name.split("（")[0].split("(")[0].split("<")[0].split("[")[0].split("【")[0].split("｛")[0].split("{")[0].split("〔")[0].split("\"")[0]
        replace_marks = [" ", "◆", "★", "*", "▲", "⊕", ")", "/", "：", "·", "〔", "■"]
        search_word = search_word.strip()
        for replace_mark in replace_marks:
            search_word = search_word.replace(replace_mark, "")
        return search_word

    def get_data(self):
        """
        获取分数线数据
        :return:
        """
        page_source = self.driver.page_source
        html = etree.HTML(page_source)
        school_name = html.xpath("//span[@class='line1-schoolName']/text()")[0]
        province, exam_type, _ = html.xpath("//div[@class='ant-select-selection-selected-value']/@title")
        trs = html.xpath("//tbody/tr")
        for tr in trs:
            year = "2018"
            max_score = tr.xpath(".//td[2]/text()")[0]
            average = tr.xpath(".//td[3]/text()")[0]
            min_score = tr.xpath(".//td[4]/text()")[0]
            batch = tr.xpath(".//td[6]/text()")[0]
            major_name = tr.xpath(".//td[1]/text()")[0]
            search_word = Crawler.get_search_word(major_name)
            data = (
                school_name, province, exam_type, year, max_score, average, min_score, batch, major_name, search_word
            )

            # 插入数据
            # self.mysql.insert(data)

    def choose_location(self):
        self.driver.get(url=self.first_url)
        change_location = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='changecity']")))
        change_location.click()

        bj = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='content-cities']/a[text()='北京市']")))
        bj.click()
        time.sleep(1)

    def choose_school(self, school_num):
        self.driver.get(self.base_url % str(school_num))
        school_name = self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='line1-schoolName']")))
        if not school_name.text:
            """
            如果没有学校名字，证明该url无效
            """
            return

        subject_div = self.wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-selection-selected-value']")))[1]
        subject_div.click()
        # self.driver.execute_script("arguments[0].click();", subject_div)
        # subject_div.send_keys(Keys.SPACE)
        time.sleep(0.5)
        subjects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
        subjects[0].click()  # 关闭下拉菜单
        self.get_data()
        self.page_down()

        for subject_num in range(1, len(subjects)):
            subject_div = self.wait.until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-selection-selected-value']")))[
                1]
            subject_div.click()  # 显示下拉菜单
            time.sleep(0.5)
            subjects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                                            "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
            subjects[subject_num].click()
            time.sleep(0.5)
            self.get_data()
            self.page_down()

        # a = input("close?")

    # def major_line(self):
    #     self.driver.get(url=self.base_url)
    #     province_div = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-selection-selected-value']")))
    #     province_div.click()
    #     provinces = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
    #     print(len(provinces))
    #     provinces[0].click()
    #
    #     subject_div = self.wait.until(
    #         EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-selection-selected-value']")))[1]
    #     subject_div.click()
    #     time.sleep(1)
    #     subjects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
    #     self.get_data()
    #     self.page_down()
    #
    #     for subject_num in range(1, len(subjects)):
    #         subject_div = self.wait.until(
    #             EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-selection-selected-value']")))[
    #             1]
    #         subject_div.click()
    #         subjects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,
    #                                                                         "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
    #         subjects[subject_num].click()
    #         time.sleep(1)
    #         self.get_data()
    #         self.page_down()
    #
    #     # 获取第一个省份的数据
    #     for i in range(1, len(provinces)):
    #         # 获取之后省份的数据
    #         province_div = self.wait.until(
    #             EC.element_to_be_clickable((By.XPATH, "//div[@class='ant-select-selection-selected-value'][1]")))
    #         province_div.click()
    #         provinces = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,
    #                                                                          "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
    #         provinces[i].click()
    #         time.sleep(1)
    #
    #         # 获取各个科类的数据
    #         subject_div = self.wait.until(
    #             EC.presence_of_all_elements_located((By.XPATH, "//div[@class='ant-select-selection-selected-value']")))[
    #             1]
    #         subject_div.click()
    #         subjects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,
    #                                                                         "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
    #         subjects[0].click()
    #         time.sleep(1)
    #         self.page_down()
    #
    #         for subject_num in range(1, len(subjects)):
    #             subject_div = self.wait.until(
    #                 EC.presence_of_all_elements_located(
    #                     (By.XPATH, "//div[@class='ant-select-selection-selected-value']")))[
    #                 1]
    #             subject_div.click()
    #             subjects = self.wait.until(EC.presence_of_all_elements_located((By.XPATH,
    #                                                                             "//div[@class='ant-select-dropdown ant-select-dropdown--single ant-select-dropdown-placement-bottomLeft'][1]/div/ul/li")))
    #             subjects[subject_num].click()
    #             time.sleep(1)
    #             self.page_down()
    #
    #     a = input("close?")

    def close(self):
        self.driver.close()

    def main(self):
        # 获取学校
        # obj = Client()
        # schools = obj.main()
        with open("schools", "r") as f:
            schools = eval(f.read())

        print(type(schools))
        print(schools)


        self.driver.get(url=self.first_url)
        change_location = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='changecity']")))
        change_location.click()
        cities = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='content-letter']/div[@class='content-province']/div[@class='content-cities']/a[1]")))
        # 切换城市，共34个
        for city in cities[0:1]:
            if city.text not in ["澳门半岛", "台北市", "香港岛", "北京市"]:
                print(city.text)
                city.click()
                for school_num in schools:
                    try:
                        self.choose_school(school_num)
                    except Exception as e:
                        print(school_num, "有问题:", e)
        self.close()
        self.mysql.close()


def main():
    crawler = Crawler()
    crawler.main()


if __name__ == '__main__':
    start = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    main()
    print(start)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

