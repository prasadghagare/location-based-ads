import json
from flask import Flask
app = Flask(__name__)

from queue import get_queue_for_user

def convertTextToJson(text):
    json_object = json.loads(text)
    return json_object

def handle_upload_bill(bill_details):
    #Check JSON blob
    try:
        bill_details_json = convertTextToJson(bill_details)
        app.logger.debug ("Json Object {}".format(bill_details_json))
    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return "Failure"
    # Insert into MySQL

    #return sucess if check and save true
    return "Success"


def handle_add_offers(offer_details):
    #Check JSON blob
    try:
        offer_details_json = convertTextToJson(offer_details)
        app.logger.debug ("Json Object {}".format(offer_details))
    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return "Failure"
    # Insert into MySQL

    #return sucess if check and save true
    return "Success"



def handle_view_offers():
    #Return list of offers from db

    # TODO: replae this with Offer object
    sample_offer = [{"location_x":22.3, "location_y":20.2 , "place":"Big Bazaar", "item":"Milk", "discount": "5"}]
    return sample_offer



def handle_add_user(user_details):
    #Check JSON blob
    try:
        user_details_json = convertTextToJson(user_details)
        app.logger.debug ("Json Object {}".format(user_details_json))
    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return "Failure"
    # Insert into MySQL

    #return sucess if check and save true
    return "Success"


def handle_view_users():
    #Return list of offers from db
    sample_users = [{"username":"sushilpatil", "phone":"9870456051","password":"sushi"}]
    return sample_users

def handle_view_user_offers(username):
    #Check JSON blob
    try:
        list_of_offers_for_user = get_queue_for_user(username)
        return list_of_offers_for_user
    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return []



# TODO:  Fix this
def handle_send_location(location_x, location_y, username, radius):
    try:
        app.logger.info("Received location info - location_x:{}, location_y:{} , username:{} , radius:{}")

        # Find list of ofeers in the radius of location_x and location_y

        # Get items that user buy

        # Find offers that match

        # Send the matching list to the queue for the user

        # if no exception send success else failure


    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return "Failure"

    #return sucess if check and save true
    return "Success"
