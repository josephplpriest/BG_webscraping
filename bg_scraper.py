import requests
from datetime import datetime as dt
import pandas as pd
import json
from scrapy import Selector
import time
# unused atm, but will add time.sleep call later to do rate-limiting for website calls


# Set up the search url conditions
base_url = "https://www.reddit.com/search/?q="
subreddit = "subreddit%3Aboardgames"
author = "%20author%3Aautomoderator"
search_terms = ['two', 'player']
base_search_url = base_url + subreddit + author


def url_supplier(day_mon_year: list, search_terms: list, base_url=base_search_url) -> tuple:
    """function to concatenate reddit search url with the date, also returns day and month for verifying post

    Args:
        day_mon_year:   day, month, year to search for, as a list
        search_terms:   search terms
        base_url:       url stub to add to, as string

    Returns:
        tuple (
        str:    the url put together
        day:    string
        month:  string
        )
    """

    day = day_mon_year[0]
    month = day_mon_year[1]
    next_search_url = '%20'.join([base_search_url] + day_mon_year + search_terms)
    return (next_search_url, day, month)


# starting with the first tuesday, select every seventh day using list slicing
tuesdays_dt = list(pd.date_range('Jan-01-2021', 'Jan-31-2022'))[4::7]
# split the dates into strings
split_list = [dt.strftime(day, "%B %d %Y").split() for day in tuesdays_dt]
# change the months to lowercase
tuesday_strings = [[string.lower() for string in y] for y in split_list]

url, day, month = url_supplier(tuesday_strings[0], search_terms)
response = requests.get(url)
# parse url response with
sel = Selector(text=response.content)

#find correct post from reddit search using date and search term info
for url in sel.xpath("//a//@href")[3:]:
    link = url.extract()
    if "https" in link \
            and day in link \
            and month in link \
            and "two" in link:
        search_result = link

response = requests.get(search_result + '.json')

print(response.status_code)

page_as_json = json.loads(response.text)


def json_extract(obj: dict, key: str) -> list:
    """Recursively fetch values from nested JSON.
    Args:
        obj: a json object or dict
        key: value to search for
    Returns:
        arr: list of dict values

    """
    arr = []

    def extract(obj, arr, key):
        """Recursively search for values of key in JSON tree."""
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


comment_list = json_extract(page_as_json, 'body')
# first author is the automoderator post
author_list = json_extract(page_as_json, 'author')[1:]

for author, comment in zip(author_list[:5], comment_list[:5]):
    print(f"{author}: {comment}")

#%%
