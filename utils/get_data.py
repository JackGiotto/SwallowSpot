def convert_date(date: str) -> str:
    """converts date from italian to american
    """
    print(date)
    splitted= date.split("-")
    print(splitted)
    day = splitted[0]
    month = splitted[1]
    year = splitted[2]
    return year + "-" + month + "-" + day