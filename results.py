# Extract Algo & NLP results from Funcationality folders

from datetime import datetime, timedelta
import os
time = datetime.now()
import pandas as pd
from runapp import Main
#Import dependencies
algo_path = r"Data/Functionality/Algo_Bot/"
twitter_sentiment = pd.read_csv('Data/Functionality/Twitter/twitter.csv')
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



total_profit = []
for algo in algo_crypto:
    total_returns = (investment_algorithm[algo]['profit'].iloc[-1])
    total_profit.append(total_returns)
total_profit = sum(total_profit)

#Twitter results
twitter_sentiment = pd.read_csv('Data/Functionality/Twitter/twitter.csv')
open_variable = 10


class print_results(Main):
    print('')
    print('')
    print(f'The top picks have a {open_variable} Average Compound Score on Reddit at {time}.') 
    print('')
    print('')
