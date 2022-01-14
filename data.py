class CurrencyData:
    def __init__(self, currency_list):
        self.funds = {cur: -1 for cur in currency_list}
        self.course = {cur: -1 for cur in currency_list}
