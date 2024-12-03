def parse_date(date):
    """
    convert string date into a tuple of ints. 
    format date": "1475-10-06"
    return a date (tuple of ints -> (year, month, date))
    some dates only have year and month or only year
    note that later on we'll have to to consider multiple dates with certainty levels 
    """
    # write code here
    date_array = [int(value) for value in date.split('-')]
    return date_array

def parse_num(num):
    """
    vol
    remove leading 0s
    return result
    """
    return int(num)

def parse_page(page):
    if not page:
        return None
    page_array = [int(value) for value in page.split(',')]
    return page_array

def parse_json(json_entries):
    """
    could be entries or entry_ids
    num types: vol, pg
    date types: date

    """
    return json_entries