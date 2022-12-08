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

uid = 'naver-id' 
upw = 'naver-password'
 
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
    key_url = 'https://cafe.naver.com/ArticleList.nhn?search.clubid=10209062&search.menuid=275&search.boardtype=L&search.totalCount=151&search.cafeId=10209062&search.page={}'.format(page)
    return key_url


data = [] 

for i in range( 1, 201 ):
    url = move_page( i )
    driver.get( url )
    
    driver.switch_to.frame('cafe_main')
    
    search_url = driver.page_source
    soup = BeautifulSoup(search_url, 'html.parser')
    
    subj_locate = '#main-area > div:nth-child(4) > table > tbody > tr:nth-child(n) > td.td_article > div.board-list > div > a.article'
    subjects = soup.select(subj_locate)
    
    for subject in subjects:
        sub = subject.text.strip()
        
        data.append(sub)
    time.sleep( random.uniform(2,4) )

c = os.path.exists( 'countryPost.txt' )    
if c:
    os.remove( 'countryPost.txt' )
        
with open( 'countryPost.txt', 'w', encoding='utf-8' ) as f:
    for line in data:
        for l in line:
            f.write( l )
        f.write( '\n' )