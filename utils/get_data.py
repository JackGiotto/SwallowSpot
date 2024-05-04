from models import db

def get_cities(want_list = False):
    cities_query = '''SELECT city_name FROM Topology;'''
    cities = db.executeQuery(cities_query)
    if not want_list:
        return cities
    cities_list = [(city['city_name']) for city in cities]
    return cities_list