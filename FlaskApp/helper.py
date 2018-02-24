import json
from flask import Flask
app = Flask(__name__)

from queue import get_queue_for_user
import logic

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
    offer = [{column_list[0]:column[0], column_list[1]:column[1],column_list[2]:column[2],column_list[3]:column[3],column_list[4]:column[4]} for column in results ]
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
    offer = [{column_list[0]:column[0], column_list[1]:column[1],column_list[2]:column[2],column_list[3]:column[3]} for column in results ]
    return offer


    return sample_users

#TODO; Since queue is not implemented get the list of offers suggested for the user
def handle_view_user_offers(username):
    #Check JSON blob
    try:
        list_of_offers_for_user = get_queue_for_user(username)
        return list_of_offers_for_user
    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return []

def handle_get_item_list():
    # select DISTINCT item from offer_details
    column_list=["DISTINCT item"]
    table ="item_list"
    query = generate_query_from_column_list(table, column_list)
    results= query_database(query)
    offer = [column[0] for column in results ]
    return offer



# TODO:  Fix this
def handle_send_location(location_x, location_y, username, radius, count,email_id):
    try:
        app.logger.info("Received location info - location_x:{}, location_y:{} , username:{} , radius:{} , count:{} , email_id:{}".format(location_x,location_y,username,radius,count,email_id))

        # Find list of offers in the radius of location_x and location_y
        #[{"item": "Milk", "location_x": "20.2", "location_y": "32.1", "place": "Big Bazaar", "discount": "10"},{}]
        offer_list_within_radius = logic.get_offer_list_within_radius(location_x,location_y,radius)

        app.logger.info("Offers within radius - {}".format(len(offer_list_within_radius)))

        # Get items that user buy
        # select item,count(*) as count from user_ocr_details where user='sushilpatil' group by item order by count desc limit 2;
        # TODO; what it returns
        #[{"item":"Milk","count":"2"},{}]
        items_that_user_buy = logic.get_items_that_user_buy(username, count)

        app.logger.info("Count of items that user buy - {}".format(len(items_that_user_buy)))


        # Find offers that match
        #[{"item": "Milk", "location_x": "20.2", "location_y": "32.1", "place": "Big Bazaar", "discount": "10"},{}]
        offers_that_match = logic.get_items_that_match(offer_list_within_radius, items_that_user_buy)
        app.logger.info("Count of offers that match - {}".format(len(offers_that_match)))


        # TODO;Send the matching list to the queue for the user
        # As of now we'll send this list to the email client to generate list of offer texts
        #["Milk at Big Bazaar for 5% discount - URL https://www.google.com/maps/search/18.9947392,72.82435190000001",""]
        offers_in_text = logic.get_offers_in_text(offers_that_match)
        app.logger.debug("Offers in text -- {}".format(offers_in_text))
        # Send offers in email format
        logic.send_email(offers_in_text,email_id)
        # if no exception send success else failure
        #return sucess if check and save true
        return "Success"

    except Exception as e:
        app.logger.error("Exception {}".format(e))
        return "Failure"
