import requests
from bs4 import BeautifulSoup
import pandas as pd
from textblob  import TextBlob

df = pd.read_csv("sony-headphones.csv")
df = pd.DataFrame(df)

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
