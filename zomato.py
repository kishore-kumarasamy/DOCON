import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

total_length = 0

def scrape(content,list_row):
    soup = BeautifulSoup(content,"html.parser")
    top_rest = soup.find_all("div",attrs={"class": "ui cards"})
    list_tr = top_rest[0].find_all("div",attrs={"class": "col-s-12"})

    rating=soup.find_all("div",attrs={"class": "ta-right floating search_result_rating col-s-4 clearfix"})
    list_rest = list_row
    id = 1

    for tr in list_tr:
        print(tr)
        dataframe ={}
        whl = False
        if tr.find('a', class_="result-title hover_feedback zred bold ln24 fontsize0 "):
            dataframe["restaurant_id"] = id + len(list_rest)
            dataframe["name"] = (tr.find('a', class_="result-title hover_feedback zred bold ln24 fontsize0 ")).text.replace('\n', ' ').strip()
            if (tr.find('a', class_="ln24 search-page-text mr10 zblack search_result_subzone left")):
                dataframe["area"] = (tr.find('a', class_="ln24 search-page-text mr10 zblack search_result_subzone left")).text.replace('\n', ' ')
            else:
                dataframe["area"] = None
            if (tr.find("div",attrs={"class": "res-snippet-small-establishment mt5"})):
                dataframe["restaurant_type"] = (tr.find("div",attrs={"class": "res-snippet-small-establishment mt5"})).text.replace('\n', ' ')
            else:
                dataframe["restaurant_type"] = None
            dataframe["Ratings"] = rating[id - 1].find("div", attrs={"data-variation": "mini inverted"}).text.replace('\n', '').strip()
            if (rating[id - 1].find('span') == None):
                dataframe["votes"] = "None"
            else:
                dataframe['votes'] = rating[id - 1].find('span').text.replace('\n', ' ').strip()

            #list_rest.append(dataframe)
            if len(list_rest)<80:
                whl = False
                list_rest.append(dataframe)
            else:
                whl = True

            #id+= 1
    return list_rest,whl

url = "https://www.zomato.com/bangalore/south-bangalore-restaurants?page="

page=1
df_list=[]
row_list = []
id = 0
counter = 0

while url:
    print(page)
    print(len(row_list))
    response1 = requests.get("https://www.zomato.com/bangalore/south-bangalore-restaurants?page=" + str(page),
                             headers=headers)
    content = response1.content
    print('page', page)
    scr = scrape(content,row_list)
    print(scr)
    val = scr[0]
    print(val)
    if scr[1]:
        break
    row_list = val.copy()
    page+=1

print(row_list)
df = pd.DataFrame(row_list)
df = df[['restaurant_id','name','restaurant_type','area','Ratings','votes']]
df.to_csv("zomato.csv",index=False)
df.to_json('Zomato_jsn.json',orient='records')
