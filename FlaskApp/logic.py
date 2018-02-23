import json
from flask import Flask
app = Flask(__name__)

from queue import get_queue_for_user

from database_utilities import query_database, insert_database , generate_query_from_column_list




def convert_lat_long_to_google_maps_url(location_x,location_y):
    return "https://www.google.com/maps/search/{},{}".format(location_x,location_y)
