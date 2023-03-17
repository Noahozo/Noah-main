from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import undetected_chromedriver as uc
import pymysql 
import pandas as pd

my_options = webdriver.ChromeOptions()
# my_options.add_argument("--headless")                #不開啟實體瀏覽器背景執行
my_options.add_argument("--start-maximized")  # 最大化視窗
my_options.add_argument("--incognito")  # 開啟無痕模式
my_options.add_argument("--disable-popup-blocking")  # 禁用彈出攔截
my_options.add_argument("--disable-notifications")  # 取消 chrome 推播通知
my_options.add_argument("--lang=zh-TW")  # 設定為正體中文
# my_options.add_argument('blink-settings=imagesEnabled=false')  # 不載入圖
my_options.add_experimental_option(
    "excludeSwitches", ['enable-automation', 'enable-logging'])  # 沒有異常log
driver = webdriver.Chrome(
    options=my_options,
    service=Service(ChromeDriverManager().install()))

host='127.0.0.1'
usr='root'
pwd='asd851216'
db='bdse28stock'

connection = pymysql.connect(host=host, port=3306, user=usr, password=pwd, database=db)
cursor = connection.cursor()
cursor.execute("DROP TABLE IF EXISTS news")

try:
    with connection.cursor() as cursor:
        # 建立 SQL 語句
        sql = """CREATE TABLE `news` (
                `news` varchar(20) NOT NULL,
                `link` varchar(200) primary key not null,
                `title` varchar(20),
                `time` datetime,
                `reporter` varchar(200),
                `article` varchar (3000) not null,
                `stocks` varchar(50)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""

        # 執行 SQL 語句
        cursor.execute(sql)
    # 提交變更
    connection.commit()
except:
    pass
    # 關閉連接
    
    # connection.close()

url = 'https://money.udn.com/money/cate/5590?from=edn_navibar'
driver.get(url)

alinks = []
results = []

def input_links():
    links=driver.find_elements(By.CSS_SELECTOR,'section> ul > li > a')
    for i in links:
        urll=i.get_attribute('href')
        alinks.append(urll)
    print(len(alinks))
def more_links():
    more= driver.find_elements(By.CSS_SELECTOR,'section > div > span.more')
    for ii in range(len(more)):
        for jj in range (100):
            try:
                more[ii].click()
                sleep(0.5)
            except:
                continue
def crawler ():
    news='經濟日報'
    link=driver.current_url

    title = driver.find_element(By.CSS_SELECTOR, '#story_art_title')
    title = title.get_attribute('innerText')

    time = driver.find_element(By.CSS_SELECTOR, '#story_anchor > div > div > section > div > article > section > time')
    time = time.get_attribute('innerText')
    
    try:
        stocks = driver.find_element(By.CSS_SELECTOR, '#story_anchor > div > div > section > div.article-layout-wrapper > section.article-keyword > ul')
        stocks = stocks.get_attribute('innerText')
        stocks = stocks.replace('\n',' ')
    except:
        stocks = 'None'
    reporter = driver.find_element(By.CSS_SELECTOR, '.article-body__info')
    reporter = reporter.get_attribute('innerText').split(' ')
    reporter = reporter[1]
    if '／' in reporter:
        reporter=reporter.split('／')
        reporter = reporter[0]

    in_text = driver.find_element(
        By.CSS_SELECTOR, '#article_body')
    in_text = in_text.get_attribute('innerText')
    article = in_text.replace('\n', ' ')
    
    connection = pymysql.connect(host=host, port=3306, user=usr, password=pwd, database=db)
    cursor = connection.cursor()
    sql = 'INSERT INTO news (news, link, title, time, reporter, article ,stocks) VALUES ("%s", "%s", "%s", "%s", "%s", "%s","%s");'\
                        % (news, link, title, time, reporter, article,stocks)
    try:
        cursor.execute(sql)
    except:
        pass
    connection.commit()
    connection.close()


if __name__ == '__main__':
    more_links()
    input_links()
    for j in range(len(alinks)):
        driver.get(alinks[j])
        sleep(2)
        crawler()