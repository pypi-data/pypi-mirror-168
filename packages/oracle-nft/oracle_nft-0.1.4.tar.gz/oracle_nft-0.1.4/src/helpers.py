import requests
from decouple import config
import datetime
import dateparser
import time
from processors import processOpensea, processLooksRare, processX2Y2
import random
from concurrent.futures import ThreadPoolExecutor


headers = {
    'opensea':
        {
            "Accept": "application/json",
            "X-API-KEY": config("OPENSEA")
        },
    'x2y2':
        {
            "Accept": "application/json",
            "X-API-KEY": config("X2Y2")
        },
    }

urls = {'opensea': "https://api.opensea.io/api/v1/events?&asset_contract_address={}&event_type=successful&occurred_before={}&occurred_after={}",

        'looksrare': "https://api.looksrare.org/api/v1/events?collection={}&type=SALE&pagination%5Bfirst%5D=150",
        
        'x2y2': "https://api.x2y2.org/v1/events?type=sale&contract={}&created_before={}&created_after={}",
        }

loans = {}


def requestOpenSea(contract, start_hours, end_hours):
    # print('Requesting OpenSea...')
    prices = []
    tokens = []
    
    start_date = time.mktime((dateparser.parse(str(start_hours) + " hours ago")).timetuple())
    end_date = time.mktime((dateparser.parse(str(end_hours) + " hours ago")).timetuple())

    opensea_data = urls["opensea"].format(contract, end_date, start_date)
    entries = requests.get(opensea_data, headers=headers["opensea"]).json()
    tokens, prices = processOpensea(entries, tokens)

    while entries["next"]:
        time.sleep(1)
        entries = requests.get(opensea_data + "&cursor=" + entries['next'], headers=headers["opensea"]).json()
        tokens_return, prices_return = processOpensea(entries, tokens)
        tokens = tokens + tokens_return
        prices = prices + prices_return

    return prices


def requestLooksRare(contract, start_hours, end_hours):
    # print('Requesting LooksRare...')
    prices = []
    tokens = []

    start_date = datetime.datetime.strptime(str(dateparser.parse(str(start_hours) + " hours ago"))[:-7], '%Y-%m-%d %H:%M:%S')
    end_date = datetime.datetime.strptime(str(dateparser.parse(str(end_hours) + " hours ago"))[:-7], '%Y-%m-%d %H:%M:%S')
    
    entries = requests.get(urls["looksrare"].format(contract)).json()
    tokens, prices, state = processLooksRare(entries, tokens, start_date, end_date)

    # Finished searching
    if state:
        pass
    else:
        while True:
            entries = requests.get(urls["looksrare"].format(contract) + "&pagination%5Bcursor%5D=" + state).json()
            tokens_return, prices_return, state = processLooksRare(entries, tokens, start_date, end_date)
            tokens = tokens + tokens_return
            prices = prices + prices_return

    return prices


def requestX2Y2(contract, start_hours, end_hours):
    # print('Requesting X2Y2...')
    prices = []
    tokens = []

    start_date = round(time.mktime((dateparser.parse(str(start_hours) + " hours ago")).timetuple()))
    end_date = round(time.mktime((dateparser.parse(str(end_hours) + " hours ago")).timetuple()))

    x2y2_data = urls["x2y2"].format(contract, end_date, start_date)
    entries = requests.get(x2y2_data, headers=headers["x2y2"]).json()
    tokens, prices = processX2Y2(entries, tokens)

    while entries["next"]:
        time.sleep(1)
        entries = requests.get(x2y2_data + "&cursor=" + entries["next"], headers=headers["x2y2"]).json()
        tokens_return, prices_return = processX2Y2(entries, tokens)
        tokens = tokens + tokens_return
        prices = prices + prices_return

    return prices


def poolParser(args):
    if 'OpenSea' == args[0]:
        overall_prices = requestOpenSea(args[1], args[2], args[3])
    elif 'LooksRare' == args[0]:
        overall_prices = requestLooksRare(args[1], args[2], args[3])
    elif 'X2Y2' == args[0]:
        overall_prices = requestX2Y2(args[1], args[2], args[3])
    
    return overall_prices


def fetchData(contract, marketplaces, start, end):
    overall_prices = []
    args = []
    print('Fetching data for contract {} in marketplaces: {}'.format(contract, marketplaces))

    for market in marketplaces:
        args.append((market, contract, start, end))

    with ThreadPoolExecutor(max_workers=3) as pool:
        response_list = list(pool.map(poolParser, args))

    overall_prices = [int(val) for sublist in response_list for val in sublist]

    # Minimal threshold for data entries
    if len(overall_prices) < 10:
        return 'Not enough data entries for oracle calculation. Please try different time windows.'

    return overall_prices


def average_list(list):
    avg = sum(list) / len(list) 
    return avg


def random_range(end, start):
    while True:
        num_list = random.sample(range(end, start), 2)
        random_difference = abs(num_list[0] - num_list[1])
        if random_difference == round((start - end) * 0.8):
            num_list.sort()
            random_end = num_list[0]
            random_start = num_list[1]

            print('Random time window: {}'.format(num_list))
            print('Random time difference: {}'.format(random_difference))
            return random_end, random_start
