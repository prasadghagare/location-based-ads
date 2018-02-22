import json
from flask import Flask
app = Flask(__name__)

from queue import get_queue_for_user

from database_utilities import query_database, insert_database , generate_query_from_column_list

def convertTextToJson(text):
    json_object = json.loads(text)
    return json_object

def handle_upload_bill(bill_details,username):
    #Check JSON blob
    try:
        bill_details_json = convertTextToJson(bill_details)
        app.logger.debug ("Json Object {}".format(bill_details_json))

        # Insert into MySQL
        # sample= "insert into user_ocr_details(user, item, count) values("sushilpatil", "Milk", 3);"

        table="user_ocr_details"
        column_list = ["user","item","count"]

        for key in bill_details_json:
            insert_query= 'insert into {} ({}) values ("{}","{}","{}")'.format(table,",".join(column_list) , username, key, bill_details_json[key])
            app.logger.debug("Insert query generated in handle_upload_bill - {}".format(insert_query))

            insert_database(insert_query)

    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return "Failure"
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
    #sample_offer = [{"location_x":22.3, "location_y":20.2 , "place":"Big Bazaar", "item":"Milk", "discount": "5"}]
    column_list=["location_x","location_y","place","item","discount"]
    table ="offer_details"
    query = generate_query_from_column_list(table, column_list)
    results= query_database(query)
    offer = json.dumps([{column_list[0]:column[0], column_list[1]:column[1],column_list[2]:column[2],column_list[3]:column[3],column_list[4]:column[4]} for column in results ])
    return offer



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
    #sample_users = [{"username":"sushilpatil", "phone":"9870456051","password":"sushi"}]

    column_list=["username","phone","password","emailid"]
    table ="user_details"
    query = generate_query_from_column_list(table, column_list)
    results= query_database(query)
    offer = json.dumps([{column_list[0]:column[0], column_list[1]:column[1],column_list[2]:column[2],column_list[3]:column[3]} for column in results ])
    return offer


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




def convert_lat_long_to_google_maps_url(location_x,location_y):
    return "https://www.google.com/maps/search/{},{}".format(location_x,location_y)