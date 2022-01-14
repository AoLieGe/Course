class CurrencyData:
    def __init__(self, currency_list):
        self.funds = {cur: 0 for cur in currency_list}
        self.course = {cur: 0 for cur in currency_list}

    def set_funds(self, currency_funds):
        # method set funds for all currencies in currency_funds dict if it exist in self.funds
        for cur, funds in currency_funds.items():
            if cur in self.funds.keys():
                self.funds[cur] = funds
