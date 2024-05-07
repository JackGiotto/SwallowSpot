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