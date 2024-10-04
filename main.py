from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd



chrome_options=webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver=webdriver.Chrome(options=chrome_options)
driver.get('https://www.99acres.com/search/property/rent?city=209&res_com=R&preference=R&referrer_section=PROPERTIES_BY_AVAILABLE_FOR&tenant_pref=SM&src=HP_WIDGET&sortby=dominance&dominantBedroom=&dominantMinBudget=&dominantMaxBudget=')
end=False
while end==False:
    try:
         WebDriverWait(driver,10).until(
             EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[4]/div[1]/div/div/div/div[5]/div'))
         )
         ok_uderstood_button=driver.find_element(By.XPATH,value='//*[@id="app"]/div/div/div[4]/div[1]/div/div/div/div[5]/div')
         ok_uderstood_button.click()

    except:
        pass

    #rent amount
    rent_raw=driver.find_elements(By.CSS_SELECTOR,value=".tupleNew__priceValWrap ")
    rent_raw=[(i.text).strip("₹ /month") for i in rent_raw]
    rent=[int(i.replace(",","")) for i in rent_raw]


    ##adress of property
    full_text=driver.find_elements(By.CLASS_NAME,value="tupleNew__propType")
    span_text=driver.find_elements(By.CLASS_NAME,value='tupleNew__bOld')
    formatted_adress=[]
    for i in range(len(full_text)) :
        formatted_adress.append(full_text[i].text.replace(span_text[i].text,''))

    formatted_adress=[i.replace(" in",'') for i in formatted_adress]


    ##size and number of bedrooms
    size_and_bedroom=driver.find_elements(By.CLASS_NAME,value="tupleNew__area1Type")
    area=[]
    bedroom=[]
    for i in range(len(size_and_bedroom)):
        if i%2==0:
            temp = size_and_bedroom[i].text.replace(" sqft", "")
            temp = temp.replace(",",'')
            area.append(temp)
        else:
            temp=size_and_bedroom[i].text.replace(" BHK","")
            bedroom.append(temp)





    #detecting a next button
    try:
        EC.presence_of_element_located((By.XPATH,'//*[@id="app"]/div/div/div[4]/div[3]/div[3]/div[3]/a'))
        next_button=driver.find_elements(By.XPATH,value='//*[@id="app"]/div/div/div[4]/div[3]/div[3]/div[3]/a')
        next_button.click()
        end=False
    except:
        end=True


driver.quit()

raw_data_df=pd.DataFrame(
    {
        "address":formatted_adress,"rent":rent,"size":area,"bedrooms":bedroom
    }
)

raw_data_df.to_csv(r"C:\Users\Acer\Desktop\udemy python projects 2024\Selenium_scraping_live_website\varanasi_renting_data.csv",index=False)