import logging
from provider import check as course_check
from provider import convert as json_convert
from provider import get as course_get
from arguments import get as arguments_get

#logging.basicConfig(level=logging.INFO)

print("Cource application started!")

response_text = course_check()
json_data = json_convert(response_text)
course = course_get(['EUR', 'USD'], json_data)
print(course)

args = arguments_get()
print(args)
