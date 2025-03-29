from models import db


def get_cities(want_list = False):
    """get all cities saved in the database

    Args:
        want_list (bool, optional): False returns a dictionary, True returns a list. Defaults to False.
    
    Returns:
        dict | list: all cities saved in the database
    """

    cities_query = '''SELECT city_name FROM Topology;'''
    cities = db.executeQuery(cities_query)
    if not want_list:
        return cities
    cities_list = [(city['city_name']) for city in cities]
    return cities_list

def get_bulletins_dates(type: str) -> dict["str", "str"]:

    if (type == "snow"):
        bulletin_type = "Snow_report"
        date = "date"
    else:
        bulletin_type = "Report"
        date = "starting_date"

    bulletins_query = f"""
                        SELECT {date}
                        FROM {bulletin_type}
                        ORDER BY {date} DESC;
                    """
    dates = db.executeQuery(bulletins_query)


    result = {}
    for elem in dates:
        index = (str(elem[date])[:10]).replace("-", "")
        result[index] = "0"
   
    return result

def convert_date(date: str, item:str = "-") -> str:
    """converts date from italian to american (used in bulletin analysis)
    """
    splitted= date.split(item)
    day = splitted[0]
    month = splitted[1]
    year = splitted[2]
    return year + "-" + month + "-" + day