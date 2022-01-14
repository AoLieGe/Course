import argparse


def get():
    parser = argparse.ArgumentParser(description="Currency course script")
    parser.add_argument("-period", dest="period", type=int, required=True,
                        help='Period of course request (minutes)')
    parser.add_argument("-debug", dest="debug", type=str, default='0',
                        help='set this to output debug info to console')
    parser.print_help()

    return parser.parse_args()
