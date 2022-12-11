import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time 
import pyperclip
import pyautogui
import random

user_agent = "user-agent header"
options = Options()
options.add_argument('user-agent=' + user_agent)
options.add_argument('--mute-audio')
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), chrome_options = options)
driver.implicitly_wait(5)

uid = '네이버id' 
upw = '네이버password'
 
url = ('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')
 
driver.get(url) 

tag_id = driver.find_element(By.CSS_SELECTOR,'#id') 
tag_id.click() 
pyperclip.copy(uid) 
print(pyperclip.paste())
pyautogui.keyDown ('command') 
pyautogui.press ('v') 
pyautogui.keyUp ('command')
time.sleep(2)

tag_pw = driver.find_element(By.CSS_SELECTOR,'#pw') 
tag_pw.click() 
pyperclip.copy(upw) 
print(pyperclip.paste())
pyautogui.keyDown ('command') 
pyautogui.press ('v') 
pyautogui.keyUp ('command')
time.sleep(2) 

login_btn = driver.find_element(By.ID,'log.login') 
login_btn.click() 
time.sleep(2)

def move_page( page ):
    key_url = 'https://cafe.naver.com/firenze?iframe_url=/ArticleSearchList.nhn%3Fsearch.clubid=10209062%26search.menuid=7%26search.media=0%26search.searchdate=all%26search.defaultValue=1%26userDisplay=15%26search.option=0%26search.sortBy=date%26search.searchBy=1%26search.query=%C6%C4%B8%AE%26search.viewtype=title%26search.page={}'.format(page)
    return key_url


data = [] 

for i in range( 1, 30 ):
    url = move_page( i )
    driver.get( url )
    
    driver.switch_to.frame('cafe_main')
    
    search_url = driver.page_source
    soup = BeautifulSoup(search_url, 'html.parser')
    
    subj_locate = '#main-area > div:nth-child(5) > table > tbody > tr:nth-child(n) > td.td_article > div.board-list > div > a.article'

    subjects = soup.select(subj_locate)
    for subject in subjects:
        tmp = ''
        subject_span = subject.select('span.head')
        for i in subject_span:
            i.decompose()
        sub = subject.text.strip()
        tmp += sub
        tmp += '|||'
        try:
            content_link = subject.attrs['href']
            content_link = 'http://cafe.naver.com' + content_link
            driver.get(content_link)
            
            driver.switch_to.default_content()
            time.sleep(1)
            driver.switch_to.frame('cafe_main')
            time.sleep(1)
            content = driver.find_element(By.CSS_SELECTOR, "div.se-main-container").text
            content = content.replace('\n','')
            content = content.replace('  ', '')
            tmp += content
            
        except Exception as e:
            tmp+='error'
        
        driver.back()
        data.append(tmp)
    time.sleep( random.uniform(2,4) )


c = os.path.exists( 'parisPost.txt' )    
if c:
    os.remove( 'parisPost.txt' )
        
with open( 'paris.txt', 'w', encoding='utf-8' ) as f:
    for line in data:
        for l in line:
            f.write( l )
        f.write( '\n' )