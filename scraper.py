import requests
import os

tmtoken = os.environ['TMTOKEN']
user = os.environ['USER1']

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

# from selenium_profiles.driver import driver as mydriver
# from selenium_profiles.profiles import profiles
from selenium.webdriver.common.by import By  # locate elements
# from selenium_profiles.utils.colab_utils import display, showscreen, show_html # virtual display
from selenium.webdriver.support.ui import Select

chrome_service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())

chrome_options = Options()
options = [
    "--headless",
    "--disable-gpu",
    "--window-size=1920,1200",
    "--ignore-certificate-errors",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
for option in options:
    chrome_options.add_argument(option)

driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


#### Get Links 

from time import sleep
from random import randint
import random
cashrainlinks = ["https://cashrain.com/",
"https://cashrain.com/",
"https://cashrain.com/explore",
"https://cashrain.com/leaderboard",
"https://cashrain.com/login",
"https://cashrain.com/register",
"https://cashrain.app/api/connect/twitch",
"https://cashrain.com/privacy",
"https://cashrain.com/terms",
"https://cashrain.com/contact",
"https://cashrain.com/bugbounty",
"https://cashrain.productlane.io/roadmap"
]

checkoutlinks = []

for i in range(6):
  loadmore = driver.find_elements(By.CLASS_NAME, "light-button")
  for elem in loadmore:
    if elem.get_attribute("textContent") == "Load more":
      elem.click()
  sleep(3+randint(1,10))
#elems = driver.find_elements_by_xpath("//a[@href]")
elems = driver.find_elements(By.XPATH, "//a[@href]")
for elem in elems:
    if elem.get_attribute("href") not in cashrainlinks:
      print(elem.get_attribute("href"))
      checkoutlinks.append(elem.get_attribute("href"))

# newlist 
newlist = []
driver.get("https://cashrain.com/explore")
# testdd= driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/main/section/div/div[1]/div[2]/select')
select = Select(driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/main/section/div/div[1]/div[2]/select')[0])
select.select_by_visible_text('Newest')
for i in range(7):
  loadmore = driver.find_elements(By.CLASS_NAME, "light-button")
  for elem in loadmore:
    if elem.get_attribute("textContent") == "Load more":
      elem.click()
  sleep(3+randint(1,10))
#elems = driver.find_elements_by_xpath("//a[@href]")
elems = driver.find_elements(By.XPATH, "//a[@href]")
for elem in elems:
    if elem.get_attribute("href") not in cashrainlinks:
      print(elem.get_attribute("href"))
      newlist.append(elem.get_attribute("href"))

print(len(newlist))#testdd[0].get_attribute("textContent")
print(len(checkoutlinks))
###showscreen(driver)
#shuffle list 
ll = checkoutlinks
ll.extend(newlist)
ll = list(dict.fromkeys(ll))
random.shuffle(ll)
checkoutlinks = ll



class ActiveCashrain:
  def __init__(self, bch, timeleft, link):
    self.bch = bch
    self.timeleft = timeleft
    self.link = link
  def __str__(self):
    return f"{self.link} {self.timeleft} {self.bch} "  
  def alert(self):
    temp = self.timeleft
    temp = temp.split(":")
    if (int(temp[0]) <= 2 ):
      if int(temp[1])>=1:
        print("importantAlert")
        message = self.link + "  " + str(self.bch) + "  " + self.timeleft
        url = f"https://api.telegram.org/bot{tmtoken}/sendMessage?chat_id={user}&text={message}"
        requests.get(url).json() # this sends the message
      # url = f"https://api.telegram.org/bot{tmtoken}/getUpdates"
      # print(requests.get(url).json())

def getData(mydata,start=0):
  for i in range(start,len(checkoutlinks)):
    print(checkoutlinks[i])
    driver.get(checkoutlinks[i])
    sleep(6+randint(1,10))
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, 500);")
#    showscreen(driver)
    isacr = driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/section[2]/div/div/div/div/h2')
    if isacr.get_attribute("textContent") == "Active Cashrain":
      timeleft = (driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/section[2]/div/div/div/div/div/div/div[2]/div[2]/span/span').get_attribute("textContent").split(" h left")[0])
      money = (driver.find_element(By.XPATH, '//*[@id="__next"]/div[2]/main/section[2]/div/div/div/div/div/div/div[2]/div[2]/div[1]/div[5]/span').get_attribute("textContent").split(" | "))
      # dollar = float(money[0].split("$")[1])
      try:
        bch = float(money[1].split(" BCH")[0])
      except(ValueError):
        if (money[1].split(" BCH")[0] == "<0.01"):
          bch = 0.001
      test1 = ActiveCashrain(bch,timeleft,checkoutlinks[i])
      test1.alert()
      mydata.append(test1)


## RUN 

mydata = []
getData(mydata)

## SORT AND SEND SUM

def mySort(e):
  return e.bch 
mydata.sort(key=mySort,reverse=True)



test = [x for x in mydata if x.bch >= 0.03]
test = [x for x in test if x.timeleft != "0:00:00"]

asdf = ""
for i in range(len(test)):
  asdf += str(test[i])+"\n"
asdf

url = f"https://api.telegram.org/bot{tmtoken}/sendMessage?chat_id={user}&text={asdf}"
requests.get(url).json()