# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to get and return parsed HTML
def get_soup(url):
    # Docker & Splash option. To run without it, replace with r = requests.get(url)
    r = requests.get('http://localhost:8050/render.html', params = {'url': url, 'wait' : 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# Initialize list to store reviews data later on
reviewlist = []

# Function that sifts through the soup element above, tries to find the tags for the data we want, then appends to the list we initialized
def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product': soup.title.text.replace('Amazon.ca:Customer reviews: ', '').strip(), 
            'date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            reviewlist.append(review)
    except:
        pass

# Function 3: loop through 1:x many pages, or until the css selector found only on the last page is found (when the next page button is greyed)
for x in range(1,20):
    soup = get_soup(f'https://www.amazon.ca/Sony-WF-1000XM3-Industry-Canceling-Wireless/product-reviews/B07T81554H/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

# Save results to a dataframe, then export as CSV
df = pd.DataFrame(reviewlist)
df.to_csv(r'sony-headphones.csv', index=False)
print('Fin.')

