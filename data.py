class CurrencyData:
    def __init__(self, currency_list):
        self.funds = {cur: 0 for cur in currency_list}
        self.course = {cur: 0 for cur in currency_list}
