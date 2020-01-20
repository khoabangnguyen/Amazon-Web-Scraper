from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
driver = webdriver.Chrome("C:\\Users\\user\\ChromeDriver\\chromedriver.exe",options=chrome_options)

prices = []
names = []
ratings = []
counts = []

#fills in the info the scraper can't find with "N/A"
def add_list (lst, num):
    if len(lst) < num:
        lst.append("N/A")
    return lst

#Remove a certain laptop from the lists    
def remove_laptop(index):
    del names[index]
    del prices[index]
    del ratings[index]
    del counts[index]

# Only keep laptops that have a desired value or higher on the basis given
def my_filter_more(base_lst, value, index):
    if index == len(base_lst):
        return "None"
    elif (base_lst[index] == "N/A") or (float(base_lst[index]) < value):
        remove_laptop(index)
        my_filter_more(base_lst, value, index)
    else:
        my_filter_more(base_lst, value, index +1)

# Only keep laptops that have a desired value or lower on the basis given
def my_filter_less(base_lst, value, index):
    if index == len(base_lst):
        return "None"
    elif (base_lst[index] == "N/A") or (float(base_lst[index]) > value):
        remove_laptop(index)
        my_filter_less(base_lst, value, index)
    else:
        my_filter_less(base_lst, value, index + 1)
        

# Get the name, prices, ratings and vote count of laptops from the first 10 pages. 
for i in range(10):
    address="""https://www.amazon.ca/s?i=electronics&bbn=677252011&rh=n%3A667823011%2Cn%3A677211011%2Cn%
            3A2404990011%2Cn%3A677252011%2Cp_n_operating_system_browse-bin%3A14083352011&page={0}&pf_rd_
            i=677252011&pf_rd_m=A1IM4EOPHS76S7&pf_rd_p=c8520d34-e520-43d7-8c22-82a3ca888253&pf_rd_r=4N9B
            TMRT2V028H19YTAV&pf_rd_s=merchandised-search-2&pf_rd_t=101&qid=1579465222&ref=sr_pg_{1}""".format(i+2, i + 2)
    #print (address)
    driver.get(address)


    content = driver.page_source
    soup = BeautifulSoup(content)

            
    #Find the desired info from the site's html code blocks and add it to the lists
    for a in soup.findAll('div', attrs = {'class': "sg-col-4-of-12 sg-col-8-of-16 sg-col-16-of-24 sg-col-12-of-20 sg-col-24-of-32 sg-col sg-col-28-of-36 sg-col-20-of-28"}):
        name = a.find ('span', attrs = {'class': "a-size-medium a-color-base a-text-normal"})
        if (not (name == None)) and name.text not in names:
            names.append(name.text)
            price = a.find('span', attrs = {'class': "a-offscreen"})
            if (not (price == None)):
                prices.append(price.text)
            rating = a.find ('span', attrs = {'class': "a-icon-alt"})
            if (not (rating == None)):
                ratings.append(rating.text[0:3])
            count = a.find ('span', attrs = {'class' : "a-size-base"})
            if (not (count == None)) and count.text.isdigit():
                counts.append(count.text)

            #Fill in any missing data with "N/A"    
            max_num = max(len(names), len(prices), len(ratings), len(counts))
            names = add_list(names, max_num)
            prices = add_list(prices, max_num)
            ratings = add_list(ratings, max_num)
            counts = add_list(counts, max_num)

#Reformat the prices for easy type conversion
prices = [p.replace('CDN$\xa0', '') for p in prices]
prices = [p.replace(',', '') for p in prices] 

#Only show laptops with price less than 500
#my_filter_less(prices, 500, 0)

#Only show laptops with rating for than 4 stars
#my_filter_more(ratings, 4, 0)

#Only show laptops with more than 100 rating votes
#my_filter_more(counts,100, 0)

#Use Panda to format the data collecte and output onto Excel spreadsheet
df = pd.DataFrame({'Product Name':names,'Price':prices, 'Rating': ratings, 'Votes': counts}) 
df.to_csv('shoppingList.csv', index=False, encoding='utf-8')



    
    
    
                      
