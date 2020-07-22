from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

import pyautogui
import os
from PIL import Image

from datetime import date

chrome_options = Options()
#chrome_options.add_extension('C:\\Users\\<username>\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Extensions\\<extension-id>\\1.27.10_1.crx') #added ADBLOCKER extension, if required add this.
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome('C:\\Users\\krish\\Downloads\\chromedriver_win32\\chromedriver.exe',options=chrome_options)
driver.get("https://epaper.eenadu.net")





telangana = driver.find_element_by_xpath("//div[@eid='1']")
telangana.click()
time.sleep(2)

element = driver.find_element_by_xpath("//a[@href='#register']")
element.click()
time.sleep(2)

email =  driver.find_element_by_xpath("//input[@id='txtNumber1']")
email.send_keys('<eenadu-email-id>') # add your eenadu newspaper email, create an account it's easy.
time.sleep(1)

password = driver.find_element_by_xpath("//input[@id='txtPassword']")
password.send_keys("<password>") #add your password
time.sleep(1)

submit =  driver.find_element_by_xpath("//button[@type='submit']")
submit.click()

pyautogui.press('enter')

time.sleep(5)

driver.refresh()
time.sleep(2)


for i in range(1,20):
    try:
        if(i<9):
            path = '//img[contains(@highres,'+"\'/TEL/5_0"+str(i+1)+'\')]'
        else:
            path = '//img[contains(@highres,'+'\'/TEL/5_'+str(i+1)+'\')]'
        
        time.sleep(2)
    
        if(i==1):
    
            pyautogui.hotkey('ctrl','shift','i')
            time.sleep(3)
            pyautogui.hotkey('ctrl','shift','p')
            time.sleep(3)
            pyautogui.typewrite('screenshot')
            time.sleep(1)
            pyautogui.press('down')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
        else:
            pyautogui.hotkey('ctrl','shift','p')
            time.sleep(3)
            pyautogui.typewrite('screenshot')
            time.sleep(1)
            pyautogui.press('down')
            time.sleep(1)
            pyautogui.press('enter')
            time.sleep(1)
        
        
        page = driver.find_element_by_xpath(path)
        actions = ActionChains(driver)
        actions.move_to_element(page)
        actions.click(page) 
        actions.perform()
    
        time.sleep(1)
    
    except:
        break


epaper = []

for file in os.listdir():
    if 'epaper' in file:
        epaper.append(file)
x = epaper.pop()
epaper.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
epaper.insert(0,x)


for i in range(0,len(epaper)):
    image1 = Image.open(epaper[i])
    im1 = image1.convert('RGB')
    im1.save('EenaduMain_'+str(i)+'.pdf')
    i+=1
    
Eenadu = []

for file in os.listdir():
    if 'EenaduMain' in file:
        Eenadu.append(file)

Eenadu.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

from PyPDF2 import PdfFileMerger, PdfFileReader
mergedObject = PdfFileMerger()
for fileNumber in range(0, len(Eenadu)):
    mergedObject.append(PdfFileReader('EenaduMain_' + str(fileNumber)+ '.pdf', 'rb'))



today = date.today()
d4 = today.strftime("%b-%d-%Y")
paper_name = "eenadupaper_"+str(d4)+".pdf"
mergedObject.write(paper_name)



froms = "<from-email>" #add from email ID.
to = "<to-email>" #add to email ID.

data = MIMEMultipart() 
data['From'] = froms
data['To'] = to
data['Subject'] = "Eenadu News paper " + str(d4)

body = "Checkout today's eenadu newspaper " + str(d4)
data.attach(MIMEText(body, 'plain'))
filename = paper_name
attachment = open(paper_name, "rb")
p = MIMEBase('application', 'octet-stream')
p.set_payload((attachment).read())
encoders.encode_base64(p)
p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
data.attach(p)
s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login(froms, "<your-password>") #add your email password
text = data.as_string()
s.sendmail(froms, to, text)
s.quit()

for file in os.listdir():
    if 'epaper' in file:
        os.remove(file)
    if 'EenaduMain' in file:
        os.remove(file)

