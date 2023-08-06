import argparse
from oracle import oracle_calculator
from web3 import Web3


marketplaces = ['OpenSea', 'LooksRare', 'X2Y2']


def check_hour(value):
    ivalue = int(value)
    if ivalue < 12 or ivalue > 720:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value. Minimum is 12 hours, and maximum is 720 hours (30 days)." % value)
    return ivalue


def check_market(market):
    if market not in marketplaces:
        raise argparse.ArgumentTypeError("%s is not a supported market." % market)
    return market


def check_contract(contract):
    if not Web3.isAddress(contract):
        raise argparse.ArgumentTypeError("%s is not a valid contract address." % contract)
    return contract


parser = argparse.ArgumentParser(description='Description of your program')
parser.add_argument('-contract','--contract', type=check_contract, help='Contract address', required=True)
parser.add_argument('-markets','--marketplaces', type=check_market, nargs='+', help='Marketplaces to query', required=True)
parser.add_argument('-start','--start_hours', type=check_hour, help='Time window start hours', required=True)
parser.add_argument('-end','--end_hours', type=check_hour, help='Time window end hours', required=True)
args = vars(parser.parse_args())

start = int(args['start_hours'])
end = int(args['end_hours'])

print('Contract: {}'.format(args['contract']))
print('Marketplaces: {}'.format(args['marketplaces']))
print('Start hours: {}'.format(start))
print('End hours: {}'.format(end))

price = oracle_calculator(args['contract'], args['marketplaces'], start, end)

print('\n----------------------')
print('Oracle price: {}'.format(price[0]))
print('Oracle volatility: {}'.format(price[1]))
print('----------------------')

# python main.py --contract '0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d' --marketplaces 'OpenSea' 'LooksRare' --start_hours 720 --end_hours 12