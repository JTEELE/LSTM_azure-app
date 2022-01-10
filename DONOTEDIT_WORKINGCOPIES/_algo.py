# Extract Algo & NLP results from Funcationality folders
from datetime import datetime, timedelta
import os
time = datetime.now()
import pandas as pd
from runapp import Main
reddit_path = r"Data/Functionality/Reddit/"
algo_path = r"Data/Functionality/Algo_Bot/"
twitter_sentiment = pd.read_csv('Data/Functionality/Twitter/subjectivity_and_polarity.csv')
extension = '.csv'

def Average(lst):
    return sum(lst) / len(lst)

def Sum(lst):
    return sum(lst) / len(lst)

def format_convert(x):
    try:
        return "{:.0%}".format(x)
    except:
        return "{:.0%}".format(float(x))

def dollar_sign(x):
    return "${:,.2f}".format(x)

file_names = []
reddit_data = {}
for root, dirs_list, files_list in os.walk(reddit_path):
    for file_name in files_list:
        if os.path.splitext(file_name)[-1] == extension:
            file_name_path = os.path.join(root, file_name)
            data = pd.read_csv(file_name_path)
            reddit_data[file_name] = data
            file_names.append(file_name)

compound_scores = []
for crypto_sentiment in file_names:
    positive = (reddit_data[crypto_sentiment]['compound'][1])
    compound_scores.append(positive)
compound_sentiment = Average(compound_scores)

#Algo strategy results
algo_crypto = []
investment_algorithm = {}
for root, dirs_list, files_list in os.walk(algo_path):
    for file_name in files_list:
        if os.path.splitext(file_name)[-1] == extension:
            file_name_path = os.path.join(root, file_name)
            data = pd.read_csv(file_name_path)
            investment_algorithm[file_name] = data
            algo_crypto.append(file_name)

#Google Results
google_corr = pd.read_csv('Data/Functionality/Google/Correlation.csv', index_col='Unnamed: 0')
google_sent = pd.read_csv('Data/Functionality/Google/Sentiments.csv')
gcrypto_trends=google_sent['crypto_choice_avg'].mean()
ginflation_trends=google_sent['inflation_headlinese_avg'].mean()
genergy_trends=google_sent['energy_consumption_avg'].mean()

total_profit = []
for algo in algo_crypto:
    total_returns = (investment_algorithm[algo]['profit'].iloc[-1])
    total_profit.append(total_returns)
total_profit = sum(total_profit)

#Twitter results
twitter_sentiment = pd.read_csv('Data/Functionality/Twitter/subjectivity_and_polarity.csv')
sentiment_counts = twitter_sentiment["Analysis"].value_counts('Positive')
subjectivity = format_convert(twitter_sentiment['Subjectivity'].mean())
polarity = format_convert(twitter_sentiment['Polarity'].mean())
try:
    positive_posts = format_convert(sentiment_counts['Positive'])
except:
    pass
try:
    neutral_posts = format_convert(sentiment_counts['Neutral'])
except:
    pass
try:
    negative_posts = format_convert(sentiment_counts['Negative'])
except:
    pass

twitter_market_sentiment = pd.read_csv('Data/Functionality/Twitter/market_sentiment_analysis.csv')
market_sentiment_counts = twitter_market_sentiment["Analysis"].value_counts('Positive')
market_subjectivity = format_convert(twitter_market_sentiment['Subjectivity'].mean())
market_polarity = format_convert(twitter_market_sentiment['Polarity'].mean())

try: 
    market_positive_posts = format_convert(market_sentiment_counts['Positive'])
except:
    pass
try:
    market_neutral_posts = format_convert(market_sentiment_counts['Neutral'])
except:
    pass
try:
    market_negative_posts = format_convert(market_sentiment_counts['Negative'])
except:
    pass
print('')
print('')
print('Import print_results()')

class print_results(Main):
    print('')
    print('')
    print(f'The top picks have a {compound_sentiment} Average Compound Score on Reddit at {time}.') 
    print('')
    print('')
    print('')
    print('')
    print('')
    print(f'Overall Crypto Market Sentiment: scanned at {time}')
    print('')
    print(f'{market_positive_posts} of their posts have a positive tone.')
    print('')
    print(f'{market_negative_posts} of their posts have a negative tone.')
    print('')
    print(f'The remaining {market_neutral_posts} of their posts have a neutral tone.')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print(f'Top Influential Icons in the Cryptocurrency market: scanned at {time}')
    print('')
    print(f'{positive_posts} of their posts have a positive tone.')
    print('')
    print(f'{negative_posts} of their posts have a negative tone.')
    print('')
    print(f'The remaining {neutral_posts} of their posts have a neutral tone.')
    print('')
    print('')
    print('')
    print('')
    print('')
    print('')
    print(f'Google Trends Scanned at {time}')
    print('')
    print(f'Crypto is trending with a sentiment score of {gcrypto_trends}.')
    print('')
    print(f'Inflation is trending with a sentiment score of {ginflation_trends}.')
    print('')
    print(f'Energy is trending with a sentiment score of {genergy_trends}.')
    print('') 
    print('')
    print('')
    print('')
    print('')

print_results()