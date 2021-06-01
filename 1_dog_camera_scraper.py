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
review_list = []

# Define the URLs & URL list (only one for now)
furbo = 'https://www.amazon.ca/Furbo-Dog-Camera-Designed-Compatible/product-reviews/B01FXC7JWQ/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
url_list = [furbo]

# Function that sifts through the soup element above, tries to find the tags for the data we want, then appends to the list we initialized
def get_reviews(soup):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
            'product': soup.title.text.replace('Amazon.ca:Customer reviews: ', '').strip(), 
            'date': item.find('span', {'data-hook': 'review-date'}).text.strip(),
            'title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
            'rating': float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
            'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
            }
            review_list.append(review)
    except:
        pass

# Function 3: for every url in url list, run the get_reviews scraper for x many pages
for url in url_list: # url list
    for page in range(1,50): # pages
        soup = get_soup(f'{url}&pageNumber={page}')
        # Amazon product name
        product = soup.title.text.replace('Amazon.ca:Customer reviews: ', '').strip()
        # Print page and product name
        print(f'Getting page {page} reviews for the {product}')
        # Run scraper
        get_reviews(soup)
        # Length of review_list = cumulative results
        c_results = len(review_list)
        # Print cumulative results
        print(f'Cumulative results: {c_results}')
        # Loop for as long as the next page button is not found
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break

# Save results to a dataframe, then export as CSV
df = pd.DataFrame(review_list)
df.to_csv(r'dog-cameras-raw.csv', index=False)

rows = len(df)
print(f'Fin: {rows} records saved to CSV')

