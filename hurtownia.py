import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse
from database1 import Database


def main():
   
    category = []
    url = 'https://www.hurtowniazabawek.pl/' 
    soup = html_access(url)

    get_categories(soup, category)      
    
    for i in category:
        page = 1
        name = get_category_name(i)
        mainlist = []
        soup1 = html_access(url)
        roducts = product_details(soup1)
        parse_price(roducts)
        
        
        # while True:
            
        #     if page == 1:
        #         url = i
        #         soup1 = html_access(url)
        #         mainlist.extend(product_details(soup1))
        #         page += 1
                    
        #     else:
        #         url = i + f'strona-{page}/'
        #         soup1 = html_access(url)
        #         if  not soup1.find_all('div',{"class": "pager"}):
        #             break
        #         mainlist.extend(product_details(soup1))
        #         page += 1
        
        # get_excel(mainlist,name)
        # db = get_sql_table(name,mainlist)
        # get_sql_values(mainlist,db.conn,name)
        
 
def html_access(url):
    headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.content,'lxml')
    return soup


def get_categories(soup, category):

    for i in soup.find_all('a',{"class" : "categorySubMenu__categoryItem col"}):
        kategorie = i['href']
        category.append(kategorie)


def get_category_name (item):

    name = urlparse(item).path.replace('/','').replace('-','_').replace('155 ','')
    return name

  
def product_details(soup):

    roducts = []
    for i in soup.find_all('div',{"class": "moreBox productIcon__descBox"}):
        
        products = {
            "name" : i.find('a',{"class":"productIcon__descNameLink"}).get_text(),
            "price" : i.find('div',{"class":"productIcon__descPrice"}).get_text(),
            "currency" : 'PLN',
            "availability" : 'YES'if i.find('i',{'class':"bialy-icon_05"}) else 'NO'
        }
        roducts.append(products)
    return roducts


def parse_price(roducts):
    for i in roducts:
        e = i['price']
        if len(e) > 8:
            e = e[-str.index(e, "ł")-1:]
        print(type(e))
    return e

def get_excel(roducts,i):
    df = pd.DataFrame(roducts)
    df.to_excel(f'{i}.xlsx',index=True)


def get_sql_table(category, mainlist):
    all_keys = set().union(*(d.keys() for d in mainlist))
    columns = " ,".join(list(all_keys))
    db = Database('Hurtownia Zabawek')
    db.create_table(f'''CREATE TABLE {category} ({columns})''')
    return db


def get_sql_values(mainlist, db, category):
    df = pd.DataFrame(mainlist)
    df.to_sql(category, db, if_exists='replace',index=False)
   
if __name__ == '__main__':    
    main()

    