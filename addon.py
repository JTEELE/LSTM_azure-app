#Get Top Influencers (PART 1)
import urllib.request
import ssl
import json
import time
import tweepy
import pandas as pd
from dotenv import load_dotenv
import pprint 
import webbrowser
import time
import os
from textblob import TextBlob
import numpy as np
import re
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
#import nltk stuff
import nltk as nltk
nltk.download('vader_lexicon')
from pycoingecko import CoinGeckoAPI
from nltk.sentiment.vader import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from string import punctuation
from collections import Counter
from nltk import ngrams
lemmatizer = WordNetLemmatizer()
load_dotenv()
cg = CoinGeckoAPI()
coins = cg.get_coins()
screener = 'CRYPTO'

#Activate environment variables
consumer_key = os.getenv("tapi_key")
consumer_secret = os.getenv("tapi_secret")
access_token = os.getenv("taccess_token")
access_secret = os.getenv("taccess_secret")
bearer_token = os.getenv("tbearer_token")


#API imports
ssl._create_default_https_context = ssl._create_unverified_context
api_key = "jaxk68993earvoogjbi86a"
pp = pprint.PrettyPrinter(indent=4)

#set coin symbol list you want social stats for 
coin_list = [
    "DOGE",
    "SHIB",
    "AVAX",
    "ADA",
    "ETH",
    "BTC",
]


#create list to store influencers & screen names in
symbol = []
twitter_handle = []

#LUNARCRUSH API
for coin in coin_list:
    url = "https://api.lunarcrush.com/v2?data=influencers&key="+api_key+"&symbol="+coin+"&limit=3"
    assets = json.loads(urllib.request.urlopen(url).read())
    for asset in assets['data']:
        #pp.pprint("Twitter Handle: "+asset['twitter_screen_name'])
        twitter_handle.append(str(asset['twitter_screen_name']))

#print influencer handles         
print("Follow These TOP Twitter Influencers for Your Coins!")
print("Twitter Handle:")
for handle in twitter_handle:
    print("@" + handle)


#env variables & keys
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAHMfVgEAAAAASHUvXW3369rt439eDRGyI30kRH8%3DsOdauUQRGVm1EDhcb3S4dqrgoXPznOo7pANyBERHaPFwzpfDaF'
consumer_key = 'mdaxrJEQIC6PdBIP3fwZIlZu8'
consumer_secret = 'LLr8ZwcqkI3O7pct7krBueMUuYjAUATp1Kjk2XvDfc3R1HO8WG'
access_token = '1314430636422311942-z7RT01poe126qH2jVMJ6WtBDdAh905'
access_secret = '7dmrc9Qw6Y5e4EVKlB3MpSLlxC8SOPl7BlzKXd2L0pDAN'

#TWEEPY API 
#create authentication object
authenticate = tweepy.OAuthHandler(consumer_key, consumer_secret)

#set the access token and secret token 
authenticate.set_access_token(access_token, access_secret)

#create api object while passing in the auth information
api = tweepy.API(authenticate, wait_on_rate_limit = True) 

#Get recent tweets from financial influencers on twitter using Tweepy
influencers = twitter_handle
#extract 15 tweets from each twitter user timeline
influencer_posts_df = pd.DataFrame()

for influencer in influencers:
    recent_posts = api.user_timeline(screen_name = influencer, count=10, tweet_mode='extended')
    data = pd.DataFrame( [tweet.full_text for tweet in recent_posts] , columns=['Tweets'])
    influencer_posts_df = influencer_posts_df.append(data)


#function to clean twitter posts
def clean_text(text):
    text= re.sub(r'@[A-Za-z0-9]+', '', text) #removes @mentions
    text = re.sub(r'#','', text) #removes the # symbol
    text = re.sub(r'RT[\s]+','', text) #removes RT
    text = re.sub(r'https?:\/\/\S+','', text) #removes hyperlink
    return text
#apply clean text
influencer_posts_df['Tweets'] = influencer_posts_df['Tweets'].apply(clean_text)

#function to get subjectivity and polarity
def get_subjectivity(text):
    return TextBlob(text).sentiment.subjectivity
    
#function to get polarity
def get_polarity(text):
    return TextBlob(text).sentiment.polarity

#new columns
influencer_posts_df['Subjectivity'] = influencer_posts_df['Tweets'].apply(get_subjectivity)
influencer_posts_df['Polarity'] = influencer_posts_df['Tweets'].apply(get_polarity)

#function to analyze polarity
def get_analysis(score):
    if score <0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    else:
        return 'Positive'
    
#create new column for analysis    
influencer_posts_df['Analysis'] = influencer_posts_df['Polarity'].apply(get_analysis)
print(influencer_posts_df)

#write to csv
influencer_posts_df.to_csv('Data/Functionality/Twitter/influencer_twitter_sentiment.csv')


# PART 2
# GET TOP RECENT TWEETS FOR COIN LIST
sources = "twitter"
symbol =[]
recent_tweets = []

#LUNAR TOP FEED
for coin in coin_list:
    url = "https://api.lunarcrush.com/v2?data=feeds&key=jaxk68993earvoogjbi86a&symbol="+coin+"&limit=5&sources="+sources
    assets = json.loads(urllib.request.urlopen(url).read())
    #pp.pprint(assets)
    for asset in assets['data']:
        #print("Symbol: " +asset['symbol'])
        symbol.append(asset['symbol'])
        #print("Text: "+asset['body'])
        recent_tweets.append(asset['body'])
        
#tweets dictionary matchin symbol - tweet
tweets_data = {'Symbol':symbol,'Tweet':recent_tweets}
#append list to dataframe
recent_tweets_df = pd.DataFrame(tweets_data, columns=['Symbol','Tweet'])

#clean tweets text
recent_tweets_df['Tweet'] = recent_tweets_df['Tweet'].apply(clean_text)


def get_compound_sent(text):
    sentiment = analyzer.polarity_scores(text)
    compound = sentiment['compound']
    return compound
def get_positive(text):
    sentiment = analyzer.polarity_scores(text)
    pos = sentiment["pos"]
    return pos
def get_negative(text):
    sentiment = analyzer.polarity_scores(text)
    neg = sentiment["neg"]
    return neg
def get_neutral(text):
    sentiment = analyzer.polarity_scores(text)
    neu = sentiment["neu"]
    return neu

recent_tweets_df['compound']=recent_tweets_df['Tweet'].apply(get_compound_sent)
recent_tweets_df['positive']=recent_tweets_df['Tweet'].apply(get_positive)
recent_tweets_df['negative']=recent_tweets_df['Tweet'].apply(get_negative)
recent_tweets_df['neutral']=recent_tweets_df['Tweet'].apply(get_neutral)

#write to CSV
recent_tweets_df.to_csv('Data/Functionality/Twitter/crypto_tweet_sentiment.csv')

# Create a list of stopwords
stop_words = stopwords.words('english')

#tokenizer
def tokenizer(text):
    """Tokenizes text."""
    sw = set(stopwords.words('english'))
    regex = re.compile("[^a-zA-Z ]")
    re_clean = regex.sub('', text)
    words = word_tokenize(re_clean)
    lem = [lemmatizer.lemmatize(word) for word in words]
    tokens = [word.lower() for word in lem if word.lower() not in sw]
    return tokens
#process
def process_text(text):
    sw = set(stopwords.words('english'))
    regex = re.compile("[^a-zA-Z ]")
    re_clean = regex.sub('', text)
    words = word_tokenize(re_clean)
    lem = [lemmatizer.lemmatize(word) for word in words]
    output = [word.lower() for word in lem if word.lower() not in sw]
    return output
#top 10 most common words 
def token_count(tokens, N=10):
    big_string = ' '.join(tokens)
    tokens = process_text(big_string)
    top_10 = Counter(tokens).most_common(10)
    top_10_df = pd.DataFrame((top_10), columns=['word','count'])
    return top_10_df


#create tokens column
recent_tweets_df['tokens']=recent_tweets_df['Tweet'].apply(tokenizer)

tokens = recent_tweets_df['Tweet']
top_10_words = token_count(tokens)
print("Top 10 words used in tweets from your coin list!")
print(top_10_words)
