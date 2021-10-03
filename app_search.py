
import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

print("PROGRAM TO FIND DETAILS OF APPS IN THE PLAY STORE")
driver = webdriver.Chrome(ChromeDriverManager().install())
url=input("ENTER THE URL OF PAGE IN THE PLAY STORE :  ")   #https://play.google.com/store/search?q=casino&c=apps&hl=es&gl=es
driver.get(url)       #enter URL of page in playstore
time.sleep(5)

links_games = []
elems = driver.find_elements_by_xpath("//a[@href]")             
for elem in elems:
    if "details?id" in elem.get_attribute("href"):                                      #to get the links for all the in the page
        links_games.append((elem.get_attribute("href")))
       
links_games = list(dict.fromkeys(links_games))

list_all_elements = []
for iteration in links_games:           #loop to get info of each app
    try:
        driver.get(iteration)
        print(iteration)
        time.sleep(3)
 
        header1 = driver.find_element_by_tag_name("h1")                                  #to get name of the app
        star = driver.find_element_by_class_name("BHMmbe")                           #to get the number of stars the app has
 
 
        others = driver.find_elements_by_class_name("htlgb")
        list_others = []
        for x in range (len(others)):
            if x % 2 == 0:
                list_others.append(others[x].text)
 
        titles = driver.find_elements_by_class_name("BgcNfc")
        comments = driver.find_element_by_class_name("EymY4b")                             #to get the comments 
 
        list_elements = [iteration,header1.text, float(star.text.replace(",",".")), comments.text.split()[0]]                 #list containing info of 1 app
        for x in range (len(titles)):
            if titles[x].text == "Installs":
                list_elements.append(list_others[x])
            if titles[x].text == "Developer":
                for y in list_others[x].split("\n"):
                    if "@" in y:
                        list_elements.append(y)
                        break
 
        list_all_elements.append(list_elements)                            #list containing lists of each app
    except Exception as e:
        print(e)

df = pd.DataFrame(list_all_elements,columns=['URL', 'Name', 'Stars', 'Comments', 'Installs', 'Email Address'])
df.to_excel('scraping_playstore.xlsx', header = True, index=False)
print(df)
