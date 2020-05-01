from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
def getContainerInfo(container):
    name = container.img['title']
    itemInfo = container.find('div',class_='item-info')

    itemBranding = itemInfo.find('div',class_ = 'item-branding')
    brandName = itemBranding.img['title']
    
    ratingTag = itemBranding.find("a",class_="item-rating")
    rating = re.search('[0-5]',ratingTag['title']).group() if ratingTag != None else None
    ratingCount = re.search('\d+',itemBranding.find("span",class_='item-rating-num').get_text()).group() if ratingTag != None else None

    priceContainer = itemInfo.find("div",class_="item-action").ul.find("li",class_="price-current")
    price = re.findall('\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})?',priceContainer.get_text())
    
    return name,brandName,rating,ratingCount,price
def convertToPandasDF(data,columns):
    name = [d[0] for d in data]
    brand = [d[1] for d in data]
    
    userRating = [d[2] for d in data]
    userCount = [d[3] for d in data]
    price = [d[4][0] for d in data]
    offer = []
    for d in data:
        if(len(d[4]) == 2):
            offer.append(d[4][1])
        else:
            offer.append(None)
    df = pd.DataFrame({columns[0]:name,columns[1]:brand,columns[2]:userRating,columns[3]:userCount,columns[4]:price,columns[5]:offer})
    
    return df
def main():
    url = 'https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card'
    response = urlopen(url)

    html = response.read()
    parsedHtml = soup(html,"html.parser")
    containerDivs = parsedHtml.find_all("div",class_= "item-container")
    data = [getContainerInfo(container) for container in containerDivs]
    columns = ['Product Name','Brand Name','Average User Rating','User Count','Price','Offer Count']
    df = convertToPandasDF(data,columns)
    df.to_excel("out.xlsx")
if __name__ == "__main__":
    main()