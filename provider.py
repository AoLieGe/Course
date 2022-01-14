import json
import requests
import logging

URL = 'https://www.cbr-xml-daily.ru/daily_json.js'


def check():
    """get data from URL and return it in text format"""

    r = requests.get(URL)
    if r and r.status_code == 200:
        print('Course received successfully')
        logging.info(r.text)

        return r.text
    else:
        logging.error(f'Course request error, http get status {r.status_code}')


# TODO responce имеет встроенный конвертер json, можно использовать его, но по документации на библиотеку
# TODO метод request.json() должен бросать JSONDecodeError при ошибке преобразования, а контекстная подсказка
# TODO не видит исключения с таким именем, поэтому использовал стандартный модуль json
def convert(response):
    """convert text http-response to json-format"""
    try:
        json_data = json.loads(response)
        return json_data
    except ValueError:
        logging.error('Json parsing error')


def get(required, json_data, currency_key="Valute", value_key="Value"):
    """return dict Currency_name: currency value for 'required' currency names

    parameters:
        required - list of currency names to get course
        json_data - http response in json format, which contain key 'currency_key' with dict of valutes info
        value_key - every value is a dict which contain key 'value_key' with current valute currency
    """
    result = {}

    currencies = json_data.get(currency_key, None)
    if not currencies:
        # TODO любая ошибка в структуре json должна генерировать исключение, а не возвращать пустой ответ?
        logging.error(f"Error in parsing json-data: key named '{currency_key}' doesn't exist in response")
        return

    for cur in required:
        if cur in currencies.keys():
            value = currencies[cur].get(value_key, None)
            if not value:
                # TODO любая ошибка в структуре json должна генерировать исключение, а не возвращать пустой ответ?
                logging.error(f"Error in parsing json-data: key named '{value_key}' doesn't exist in response")
                return

            result[cur] = value
    return result
