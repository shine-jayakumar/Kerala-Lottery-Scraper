from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC, wait
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager

from datetime import datetime
import pandas as pd
import tempfile

import smtplib
from email.message import EmailMessage
import os
import sys



# Use this if you want the driver to be loaded automatically
# driver = webdriver.Chrome(ChromeDriverManager().install())

# Use this to run the script locally 
# driver_path = 'D:\chromedriver\93\chromedriver.exe'


chrome_options = webdriver.ChromeOptions()

# Use this when you're deploying script to Heroku
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

# Use this when you're deploying script to Heroku
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

# Use this line when you're running the script locally 
# driver = webdriver.Chrome(driver_path, options=chrome_options)

def wait_till(attr, attrtype, timeout):
    try:
        element_present = ''
        if attrtype.lower() == 'link_text':
             element_present = EC.presence_of_element_located((By.LINK_TEXT, attr))
        elif attrtype.lower() == 'id':
            element_present = EC.presence_of_element_located((By.ID, attr))
        elif attrtype.lower() == 'class':
            element_present = EC.presence_of_element_located((By.CLASS_NAME, attr))
        elif attrtype.lower() == 'xpath':
            element_present = EC.presence_of_element_located((By.XPATH, attr))


        if element_present != '':
                WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        pass
        # print(f'wait_till: timed out for {attr} type: {attrtype}')



def get_lottery_links(tbody_xpath):

    lottery_links = {
        'lot_name':[],
        'draw_id':[],
        'link':[]
    }

       # tr in the tbody
    lottery_rows = tbody_xpath.find_elements(By.TAG_NAME, 'tr')

    
    for row in lottery_rows:
        try:
            td_elems = row.find_elements(By.TAG_NAME, 'td')
            colnames= [key for key in lottery_links.keys()]

            for (key,td) in zip(colnames, td_elems):
                if key == 'link':
                    lottery_links[key].append(td.find_element(By.LINK_TEXT, 'View').get_attribute('href'))
                else:
                    lottery_links[key].append(td.text)

        except NoSuchElementException:
            pass

    return lottery_links


def send_email(fdata):
    

    receiver_email = os.environ.get('DEFAULT_RECEIVER_EMAIL')
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

    # when working locally SET EMAIL_ADDRESS,EMAIL_PASSWORD, and DEFAULT_RECEIVER_EMAIL
    # by setting the ENVIRONMENT VARIABLES on your local machine

 
    # if email address supplied as command-line argument
    if len(sys.argv) > 1:
        receiver_email = sys.argv[1]

    msg = EmailMessage()
    msg['Subject'] = f'Kerala Lottery Scraped - {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}'
    msg['To'] = receiver_email
    msg.set_content(f'Kerala Lottery Scraped on {datetime.now().strftime("%m/%d/%Y %H:%M:%S")}')
    
    file_data = fdata
    file_type = "text/csv"
    file_name = f'kl_{datetime.now().strftime("%m/%d/%Y %H:%M:%S")}.csv'
    msg.add_attachment(file_data, maintype='text', subtype=file_type, filename=file_name)
    try:

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg) # note that we're not using sendmail but send_message

    except Exception as e:
        pass
    



driver.get('http://www.keralalotteries.com/index.php/quick-view/result')

driver.switch_to.default_content()


# wait till the iframe loads
wait_till('blockrandom', 'id', 10)

# go to the source link of the iframe
lottery_iframe_src = driver.find_element(By.ID, 'blockrandom').get_attribute('src')
driver.get(lottery_iframe_src)

# wait till click here button is available
wait_till('Click here', 'linktext', 10)

driver.find_element_by_link_text('Click here').click()

# wait till the select is loaded
wait_till('lotterydet', 'id', 10)

lottery_df = pd.DataFrame(columns=['lot_name', 'draw_id', 'links'])

lottery_select = driver.find_element(By.ID, 'lotterydet')
no_of_lottries = len(lottery_select.find_elements(By.TAG_NAME, 'option'))



for index in range(0, no_of_lottries):
    # select element
    lottery_select_elem = driver.find_element(By.ID, 'lotterydet')
    lottery_dropdown = Select(lottery_select_elem)
    lottery_dropdown.select_by_index(index)

    wait_till('//form[@id="form1"]/table/tbody/tr/td/fieldset/table/tbody/tr[3]/td[2]/div[2]/table/tbody', 'xpath', 10)

    # tbody - OLD
    old_lottries_tbody = driver.find_element(By.XPATH, '//form[@id="form1"]/table/tbody/tr/td/fieldset/table/tbody/tr[3]/td[2]/div[2]/table/tbody')
    
    # tbody - NEW
    new_lottries_tbody = driver.find_element(By.XPATH, '//form[@id="form1"]/table/tbody/tr/td/fieldset/table/tbody/tr[3]/td[3]/div[2]/table/tbody')

    if len(lottery_df) == 0:
        lottery_df = pd.DataFrame.from_dict(get_lottery_links(old_lottries_tbody))
    else:
        lottery_df = lottery_df.append(pd.DataFrame.from_dict(get_lottery_links(old_lottries_tbody)), ignore_index=True)
    
    lottery_df = lottery_df.append(pd.DataFrame.from_dict(get_lottery_links(new_lottries_tbody)), ignore_index=True)



# print('Writing to Excel')
# lottery_df.to_excel('lottery_links_temp.xlsx')

# creating a tempfile
tmpf = tempfile.SpooledTemporaryFile()

# converting the csv created by df to bytes before writing to tempfile
tmpf.write(bytes(lottery_df.to_csv(index=False), 'utf-8'))

tmpf.seek(0)
csvfile = tmpf.read()

send_email(csvfile)

print(csvfile.decode('utf-8'))

