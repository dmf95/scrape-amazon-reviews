# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL setup and HTML request
url = 'https://www.ebay.ca/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=mcdavid+young+guns+psa+10+-checklist+-foil+-canvas+-jumbo+-beckett+-bgs9.5&_sacat=0&LH_TitleDesc=0&_osacat=0&_odkw=mcdavid+young+guns+psa+10&LH_Complete=1&rt=nc&LH_Sold=1'
r = requests.get(url)
#print(r)

# Parsing the HTML content
soup = BeautifulSoup(r.text, 'html.parser')
#print(soup)

# Getting desired data from our parsed soup
reviews = soup.find_all('div', {'class': 's-item__info clearfix'})
print(reviews)
'''
# Initialize list
data = []

# For every item in review, scrape the following data points and store as a list called review
for item in reviews:
    review = {
    # scrape product name
    'product': soup.title.text.replace('Amazon.ca:Customer reviews: ', '').strip(), 
    # scrape the review title
    'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
    # scrape the date (includes the syntax: Reviewed in Canada on...)
    'date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
    # scrape the star rating, leave as a decimal
    'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
    # scrape the actual review text
    'text': item.find('span', {'data-hook': 'review-body'}).text.strip(),
    }
    data.append(review)  
#print(len(data))

# Save results to a dataframe, then export as CSV
df = pd.DataFrame(data)
df.to_csv(r'sony-headphones.csv', index=False)

'''