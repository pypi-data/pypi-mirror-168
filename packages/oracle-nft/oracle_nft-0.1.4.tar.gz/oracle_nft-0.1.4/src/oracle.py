from helpers import fetchData, average_list, random_range
import numpy as np
import os
import csv
from datetime import datetime
import math


def oracle_calculator(contract, marketplaces, start, end):
    file = './cache/{}.csv'.format(contract)

    # Check if cache file exists
    if os.path.isfile(file):
        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                date = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S.%f')
                final_price = int(row[1])
                volatility = float(row[2])

        # Check if cached data is one day old
        if (datetime.now() - date).days > 1:
            # 24 hours have passed
            pass
        else:
            # Date is within 24 hours
            return final_price, volatility

    end_hours, start_hours = random_range(end, start)
    price_entries = fetchData(contract, marketplaces, start_hours, end_hours)

    log_returns = [math.log(number) for number in price_entries]
    volatility = np.std(log_returns) * 100

    print('Received query list:')
    print(price_entries)
    print('\nData filtering...\n')

    average = average_list(price_entries)

    # Data filtering
    for price in price_entries:
        if price < 0.1 * average or price > 9 * average:
            print('Removing price {} as it is a extremely low or high value'.format(price))
            price_entries.remove(price)
    
    price_entries.sort()

    # Truncated average with 10%
    number_to_remove = round(len(price_entries) * 0.1)
    price_entries = price_entries[number_to_remove:-number_to_remove]

    truncated_average = average_list(price_entries)
    truncated_std = np.std(price_entries)

    print("Truncated standard deviation of list: % s "% (truncated_std))
    print("Truncated average of list: {}\n".format(truncated_average))

    prices = []
    sensitivity = 1

    for price in price_entries:
        if truncated_average - (sensitivity * truncated_std) <= price <= truncated_average + (sensitivity * truncated_std):
            prices.append(price)

    print('Final price list: ')
    print(prices)

    final_price = int(np.format_float_positional(average_list(prices), trim='-'))

    if not os.path.exists("./cache"):
        # Create a new directory because it does not exist
        os.makedirs("./cache")

    f = open(file, "w+")
    f.write("{},{},{}".format(datetime.now(), final_price, volatility))
    f.close()

    return final_price, volatility
