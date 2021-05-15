import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob  import TextBlob

reviewlist = []

def get_soup(url):
    r = requests.get('http://localhost:8050/render.html', params={'url': url, 'wait': 2})
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup


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

# method = loop through 1:x many pages, or until the css selector found only on the last page is found (when the next page button is greyed)
for x in range(1,5):
    soup = get_soup(f'https://www.amazon.ca/Sony-WF-1000XM3-Industry-Canceling-Wireless/product-reviews/B07T81554H/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={x}')
    print(f'Getting page: {x}')
    get_reviews(soup)
    print(len(reviewlist))
    if not soup.find('li', {'class': 'a-disabled a-last'}):
        pass
    else:
        break

# turn reviews into a dataframe
df = pd.DataFrame(reviewlist)

'''
df.to_csv(r'sony-headphones.csv', index=False)
print('Fin.')
'''

# initialize a new dataframe to collect the sentiment scores
new_df = []
# for every review in the df, create a few columns from the verbatim blob (== body) variable
for rev in df['body']:
    blob = TextBlob(str(rev))
    score = {
        'product': df['product'],
        'date': df['date'],
        'title': df['title'],
        'rating': df['rating'],
        'text': df['body'],
        'polarity': blob.sentiment.polarity,
        'subjectivity': blob.sentiment.subjectivity
    }
    new_df.append(score)
    #print(score)

# turn the new_df 
test = pd.DataFrame(new_df)

# remove rows where polarity = 0.000
test = test[(test.polarity != 0.0000)]

'''
# test result
print(test.head())
'''

test.to_csv(r'sentiment_reviews.csv', index=False)
print('Fin.')
