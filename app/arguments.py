import argparse


class AppArguments:
    def __init__(self, currencies: list):
        self.parser = argparse.ArgumentParser(description="Currency course script")
        self._set_script_args(currencies)

    def read(self) -> dict:
        """return dict with command line arguments and values"""
        return vars(self.parser.parse_args())

    def _set_script_args(self, currencies: list) -> None:
        """set application arguments
            -period X       X (int) - period (min) of course requests
            -debug X        X (str) - if value = (1, true, True, y, Y), set debug logging level
            -currency_name  X (float) - get currency starting funds (for each in currencies list)
        """

        self.parser.add_argument("-period", dest="period", type=int, required=True,
                                 help='Period of course request (minutes)')
        self.parser.add_argument("-debug", dest="debug", type=str, default='0',
                                 help='set this to output debug info to console')

        currencies_set = set(currencies)
        for cur in currencies_set:
            self.parser.add_argument(f'-{cur}', dest=f"{cur}", type=float)
