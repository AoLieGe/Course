from arguments import AppArguments
from debug import set_debug_level
from model import CurrencyData
from impl import CourseServer


if __name__ == '__main__':
    print("Message:  Course application started!\n")
    currency_list = ['USD', 'EUR', 'RUB']

    # init data model
    currency_data = CurrencyData(currency_list)

    # read app cmd line arguments to dict
    args = AppArguments(currency_list).read()

    # extract values from parameters
    debug_status = args['debug']
    provide_delay = args['period']
    currency_funds = {c: f for c, f in args.items() if c in currency_list}

    # set values
    set_debug_level(debug_status)
    currency_data.set_funds(currency_funds)

    # create server instance and start it
    server = CourseServer(currency_data, provide_delay)
    server.start('localhost', 8080)
