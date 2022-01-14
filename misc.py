import logging

VALUTE = "Valute"  # json contain key 'VALUTE' with dict of currencies info
VALUE = "Value"  # each currency is a dict which contain key 'VALUE' with current currency value


def get_currency_values(required_currencies, json_data):
    """return dict {Currency_name: currency_value} for required_currencies currency names"""
    result = {}

    try:
        currencies = json_data[VALUTE]
        # TODO исходный список валют и валюты в URL могут иметь разный case, что тоже вызовет KeyError
        result = {c: currencies[c][VALUE] for c in required_currencies if c in currencies.keys()}
    except KeyError:
        # TODO любая ошибка доступа к json должна генерировать исключение, а не возвращать пустой ответ?
        logging.exception(f"Error in parsing json-data: key error")

    return result
