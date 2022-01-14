import argparse
import logging
import asyncio
from arguments import set_script_args
from impl import Course
from data import CurrencyData


def set_debug(param):
    if param in [1, 'true', 'True', 'y', 'Y']:
        logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':
    print("Cource application started!")
    currency_list = ['USD', 'EUR', 'RUB']
    currency_data = CurrencyData(currency_list)

    parser = argparse.ArgumentParser(description="Currency course script")  # create app arg parser
    set_script_args(parser, currency_list)  # set app arguments
    args = parser.parse_args()  # parse arguments

    args_dict = vars(args)  # convert arguments to dict
    set_debug(args_dict['debug'])  # set debug status from arguments

    currency_funds = {c: f for c, f in args_dict.items() if c in currency_list}  # get dict of currency funds
    currency_data.set_funds(currency_funds)

    course = Course(currency_data)

    # testing of course requests
    asyncio.get_event_loop().run_until_complete(asyncio.gather(course.provider(6), course.informer(10)))

