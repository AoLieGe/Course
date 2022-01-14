import itertools
import logging


class CurrencyData:
    def __init__(self, currency_list):
        self.funds = {cur: 0 for cur in currency_list}
        self.course = {cur: 1 for cur in currency_list}
        self.is_data_changed = False

    def set_funds(self, currency_funds):
        # method set funds for all currencies in currency_funds dict if it exist in self.funds
        for cur, funds in currency_funds.items():
            if cur in self.funds.keys() and self.funds[cur] != funds:
                self.funds[cur] = funds
                self.is_data_changed = True

    def set_course(self, currency_course):
        # method set course for all currencies in currency_course dict if it exist in self.course
        for cur, course in currency_course.items():
            if cur in self.course.keys() and self.course[cur] != course:
                self.course[cur] = course
                self.is_data_changed = True

    def get_all(self):
        funds = '\n'.join([f'{cur}: {funds}' for cur, funds in self.funds.items()])

        combinations = itertools.combinations(self.course.keys(), 2)
        courses = '\n'.join([f'{c[0]}-{c[1]}: {round(self._get_combination_course(c), 2)}' for c in combinations])

        base_sum = sum([funds * self.course[cur] for cur, funds in self.funds.items()])
        all_sum = {cur: base_sum / self.course[cur] for cur in self.course.keys()}
        text_sum = 'sum: ' + ' / '.join([f'{round(summ, 2)} {cur}' for cur, summ in all_sum.items()])

        return f'{funds}\n\n{courses}\n\n{text_sum}'

    def _get_combination_course(self, combination):
        return self.course[combination[0]] / self.course[combination[1]]
