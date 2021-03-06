import json
from flask import Flask
app = Flask(__name__)

from queue import get_queue_for_user

from database_utilities import query_database, insert_database , generate_query_from_column_list

from geopy.distance import vincenty
import time

import yaml
import requests




def get_offer_list_within_radius(location_x, location_y, radius):
    app.logger.debug("Inside get_offer_list_within_radius")
    # Find list of offers in the radius of location_x and location_y
    #[{"item": "Milk", "location_x": "20.2", "location_y": "32.1", "place": "Big Bazaar", "discount": "10"},{}]
    def within_radius(current_x,current_y,x,y,radius):
        app.logger.debug("Checking if ({},{}) and ({},{}) are within the radius- {}".format(current_x,current_y,x,y,radius))
        radius = float(radius)
        old_location = (current_x, current_y)
        new_location = (x,y)
        distance = vincenty(old_location,new_location).km
        return True if distance <= radius else False
    column_list=["location_x", "location_y", "place", "item", "discount"]
    table ="offer_details"
    query = generate_query_from_column_list(table, column_list)
    results= query_database(query)
    offer = [{column_list[0]:column[0], column_list[1]:column[1],column_list[2]:column[2],column_list[3]:column[3],column_list[4]:column[4]} for column in results if within_radius(location_x,location_y,column[0],column[1],radius)]
    return offer

def get_items_that_user_buy(username, count):
    app.logger.debug("Inside get_items_that_user_buy")
    # Get items that user buy
    # select item,count(*) as count from user_ocr_details where user='sushilpatil' group by item order by count desc limit 2;
    # TODO; what it returns
    #[{"item":"Milk","count":"2"},{}]
    column_list=["item","count(*) as count"]
    table ="user_ocr_details where user='{}' group by item order by count desc limit {}".format(username,count)
    query = generate_query_from_column_list(table, column_list)
    results= query_database(query)
    items = [{column_list[0]:column[0], column[1]:column[1]} for column in results]
    return items


def get_items_that_match(offer_list_within_radius, items_that_user_buy):
    app.logger.debug("Inside get_items_that_match")
    app.logger.debug("Offers within radius - {}".format(offer_list_within_radius))
    app.logger.debug("items that user buy - {}".format(items_that_user_buy))
    # Find offers that match
    #[{"item": "Milk", "location_x": "20.2", "location_y": "32.1", "place": "Big Bazaar", "discount": "10"},{}]
    """
    items_that_match=[]
    for i in offer_list_within_radius:
        for j in items_that_user_buy:
            if i['item'] == j['item']:
                items_that_match.append()
            app.logger.debug("Formattttt {}".format())
    """
    items_that_match = [i for i in offer_list_within_radius for j in items_that_user_buy if i["item"]==j["item"]]
    return items_that_match


def get_offers_in_text(offers_that_match):
    app.logger.debug("Inside get_offers_in_text")
    # TODO;Send the matching list to the queue for the user
    # As of now we'll send this list to the email client to generate list of offer texts
    #Input offers_that_match = [{'item': 'Milk', 'location_x': '20.2', 'location_y': '32.1', 'place': 'Big Bazaar', 'discount': '10'}]
    #["Milk at Big Bazaar for 5% discount - URL https://www.google.com/maps/search/18.9947392,72.82435190000001",""]
    app.logger.info("Converted offers to text for sending inemail")
    return ["{} at {} for {}% discount - {}".format(i["item"],i["place"],i["discount"],convert_lat_long_to_google_maps_url(i["location_x"],i["location_y"])) for i in offers_that_match]




def send_email(offers_in_text,email_id):
    app.logger.debug("Inside send_email")
    # Send offers in email format
    #Limit 300
    api_key=""

    def send_simple_message(api_key, text,email_id):
        return requests.post(
            "https://api.mailgun.net/v3/sandboxc82a84f981134d9b939a1bd32caad82c.mailgun.org/messages",
            auth=("api", api_key),
            data={"from": "Mailgun Sandbox <postmaster@sandboxc82a84f981134d9b939a1bd32caad82c.mailgun.org>",
                  "to": email_id,
                  "subject": "LBA - Offers for you at {}".format(time.strftime("%c")) ,
                  "text": text})
    try:
        with open('api_keys.yaml', 'r') as f:
            doc=yaml.load(f)
        api_key = doc["email_api_key"]
    except Exception as e:
        app.logger.error("No key found in FlaskApp/api_keys.yaml cannot send message {}".format(e))
        raise Exception("Couldn't send email")


    text="\n".join(offers_in_text)
    app.logger.info("Sending email to the emailid {} using api_key {}".format(email_id,api_key))
    app.logger.debug("Email contents {}".format(text))
    try:
        response = send_simple_message(api_key, text,email_id)
        app.logger.info("Email sent with response {}".format(response))
    except Exception as e:
        app.logger.error("Couldnt send email due to {}".format(e))
        raise Exception("Couldn't send email")






def convert_lat_long_to_google_maps_url(location_x,location_y):
    return "https://www.google.com/maps/search/{},{}".format(location_x,location_y)
