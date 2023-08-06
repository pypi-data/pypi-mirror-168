from datetime import datetime


def processOpensea(entries, stored):
    # print('Stored tokens: ' + str(stored))
    prices = []
    tokens = []

    for entry in entries['asset_events']:   
        # check that its sold in eth, quantity one, is_private == false and id is not seen before
        if entry['is_private'] == False and entry['quantity'] == '1' and entry['payment_token']['symbol'] == 'ETH' and entry['asset']['token_id'] not in stored:
            # print()
            # print('Token ID: {}'.format(entry['asset']['token_id']))
            # print('Price  (Wei): {}'.format(entry['total_price']))
            prices.append(entry['total_price'])
            tokens.append(entry['asset']['token_id'])

    return tokens, prices


def processLooksRare(entries, stored, start, end):
    # print('Stored tokens: ' + str(stored))
    prices = []
    tokens = []
    next_page = ''

    for entry in entries['data']:
        if entry['order']['amount'] == 1 and entry['order']['currencyAddress'] == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2' and entry['token']['tokenId'] not in stored:
            date = datetime.strptime((entry['createdAt'].replace('T', ' '))[:-5], '%Y-%m-%d %H:%M:%S')
            if start <= date <= end:
                # print()
                # print('Token ID: {}'.format(entry['token']['tokenId']))
                # print('Price  (Wei): {}'.format(entry['order']['price']))
                # print('Date: {}'.format(date))
                # print()

                next_page = entry['id']
                prices.append(entry['order']['price'])
                tokens.append(entry['token']['tokenId'])
            else:
                # print('Reached end with date: ' + str(date))
                return tokens, prices, True

    return tokens, prices, next_page


def processX2Y2(entries, stored):
    # print('Stored tokens: ' + str(stored))
    prices = []
    tokens = []

    for entry in entries['data']:
        # check that its sold in eth, quantity one, bundle == false and id is not seen before
        if entry['order']['amount'] == 1 and entry['order']['currency'] == '0x0000000000000000000000000000000000000000' and entry['order']['is_bundle'] == False and entry['token']['token_id'] not in stored:
            # print()
            # print('Token ID: {}'.format(entry['token']['token_id']))
            # print('Price  (Wei): {}'.format(entry['order']['price']))
            prices.append(entry['order']['price'])
            tokens.append(entry['token']['token_id'])

    return tokens, prices