def set_script_args(parser, currencies):
    # method add base app arguments: period and debug
    # and add all currency values arguments
    parser.add_argument("-period", dest="period", type=int, required=True,
                        help='Period of course request (minutes)')
    parser.add_argument("-debug", dest="debug", type=str, default='0',
                        help='set this to output debug info to console')

    currencies_set = set(currencies)
    for cur in currencies_set:
        parser.add_argument(f'-{cur}', dest=f"{cur}", type=float)
