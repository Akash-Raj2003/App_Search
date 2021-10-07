import pandas as pd
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

print("PROGRAM TO SCRAPE APPS IN THE PLAY STORE")
time.sleep(2)                                                                                                          #test links
url=input("ENTER THE URL OF PAGE IN THE PLAY STORE :  ")   #https://play.google.com/store/search?q=casino&c=apps&hl=es&gl=es     https://play.google.com/store/apps/collection/cluster?clp=ogoKCAEqAggBUgIIAQ%3D%3D:S:ANO1ljJG6Aw&gsr=Cg2iCgoIASoCCAFSAggB:S:ANO1ljLKNqE&hl=en_US&gl=US
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)       #enter URL of page in playstore
time.sleep(3)
scrool_num=int(input("ENTER \n 1 TO SCRAPE 50 APPS FROM  THE PLAY STORE \n 2 TO SCRAPE 100 APPS FROM THE PLAY STORE \n 3 TO SCRAPE 150 APPS FROM THE PLAY STORE \n 4 TO SCRAPE 200 APPS FROM THE PLAY STORE \n ENTER NUMBER : "))
for i in range(1,scrool_num):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")       #to scroll to the end of the page
    time.sleep(3)
    
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
df.to_excel('scraping_playstore_final.xlsx', header = True, index=False)
print(df)

options="ENTER: \n 1 TO ADD NEW ROWS TO THE DATAFRAME \n 2 TO INSERT A NEW COLUMN TO THE DATAFRAME \n 3 TO DELETE A ROW IN THE DATAFRAME \n 4 TO DELETE A COLUMN IN THE DATAFRAME \n 5 TO ACCESS A SPECIFIC ROW \n 6 TO ACCESS A SPECIFIC COLUMN \n 7  TO EXIT  \n ENTER NUMBER : "
df=pd.read_excel("scraping_playstore_final.xlsx") 
print(df)
x=int(input(options))
print("*"*100)
while True:
    if x==1:
        row_idx=input("ENTER THE LOCATION OF THE ROW")
        row_num=int(input("ENTER THE NUMBER OF VALUES IN THE ROW"))
        row_vals_lst=[]
        for i in range(0,row_num):
            row_val=input("ENTER VALUE : ")                              
            row_vals_lst.append(row_val)
        df.loc[row_idx]=row_vals_lst
        print(df)
        print("*"*100)
        x=int(input(options))
        print("*"*100)
    if x==2:
        col_name=input("ENTER THE NAME OF THE NEW COLUMN : ")
        col_idx=int(input("ENTER INDEX OF NEW COLUMN : "))
        col_val=input("ENTER VALUES IN NEW COLUMN : ") 
        df.insert(col_idx,col_name,col_val)                                                        
        print(df)
        print("*"*100)
        x=int(input(options))
        print("*"*100)
    if x==3:
        row_num=int(input("ENTER NUMBER OF ROWS TO BE DELETED"))
        del_row_lst=[]
        for i in range(0,row_num):
            del_row=int(input("ENTER INDEX OF ROW :"))
            del_row_lst.append(del_row)
        print("LIST OF ROWS TO BE DELETED= ",del_row_lst)
        df.drop(del_row_lst,axis=0, inplace= True)                                          
        print(df)
        print("*"*100)
        x=int(input(options))
        print("*"*100)
    if x==4:
        del_col_lst=[]
        print("NAME OF COLUMNS ARE",df.columns)
        column_num=int(input("ENTER THE NUMBER OF COLUMNS TO BE DELETED"))                                         
        for i in range(0,column_num):
            del_col=input("ENTER NAME OF COLUMN")                                                        
            del_col_lst.append(del_col)
        print("LIST OF COLUMNS TO BE DELETED",del_col_lst)                                   
        df.drop(del_col_lst,axis=1,inplace=True)
        print(df)
        print("*"*100)
        x=int(input(options))
        print("*"*100)
    if x==5:
        row_idx=int(input("ENTER THE INDEX OF THE DESIRED ROW "))
        print("*"*100)
        print(df.iloc[row_idx])                                                                                                        
        print("*"*100)
        x=int(input(options))
        print("*"*100)
    if x==6:
        print("NAME OF COLUMNS ARE",df.columns)
        col_name=input("ENTER NAME OF COLUMN : ")
        print(df[col_name])
        print("*"*100)                                                       
        x=int(input(options))
        print("*"*100)
    if x==7:
        print("THANK YOU")
        print("*"*100)                                        
        break

