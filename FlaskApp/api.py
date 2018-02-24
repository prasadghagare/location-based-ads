from flask import Flask, render_template, request, abort
import helper
app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')

@app.route("/uploadbill", methods=["POST"])
def upload_bill():
    if request.method == 'POST':
        app.logger.info("Received in POST message for billdetails : {} ".format(request.args))

        bill_details_json = request.args["billdetails"]
        username = request.args["username"]
        #print ("Json : {}".format(bill_details_json))

        return helper.handle_upload_bill(bill_details_json,username)


@app.route("/addoffer", methods=["POST"])
def add_offer():
    if request.method == 'POST':
        app.logger.info("Received in POST message for add_offer : {} ".format(request.args))

        offer_json = request.args["offer"]
        #print ("Json : {}".format(bill_details_json))

        return helper.handle_add_offers(offer_json)

@app.route("/viewoffers")
def view_offers():
    list_of_offers = helper.handle_view_offers()
    #return str(list_of_offers)
    return render_template('view_list.html',list = list_of_offers if len(list_of_offers)>0 else "Empty response")

@app.route("/adduser", methods=["POST"])
def add_user():
    if request.method == 'POST':
        app.logger.info("Received in POST message for user : {} ".format(request.args))

        user_json = request.args["user_details"]
        #print ("Json : {}".format(bill_details_json))

        return helper.handle_add_user(user_json)

@app.route("/viewusers")
def view_users():
    list_of_users = helper.handle_view_users()
    #return str(list_of_users)
    return render_template('view_list.html',list = list_of_users if len(list_of_users)>0 else "Empty response")

@app.route("/viewuseroffers", methods=["GET"])
def  view_user_offers():
    if request.method == 'GET':
        app.logger.info("Received in GET message for view_user_offers : {} ".format(request.args))

        username = request.args["username"]
        #print ("Json : {}".format(bill_details_json))

        list_of_offers_for_user = helper.handle_view_user_offers(username)
        return render_template('view_list.html',list = list_of_offers_for_user if len(list_of_offers_for_user)>0 else "Empty response")



@app.route("/sendlocation", methods=["POST"])
def send_location():
    if request.method == 'POST':
        app.logger.info("Received in POST message for location_x and location_y : {} ".format(request.args))

        location_x = request.args["location_x"]
        location_y = request.args["location_y"]
        username = request.args["username"]
        radius = request.args["radius"] # Can instead configure system wide , but for demo purpose using it in the HTTP
        count = request.args["count"]
        email_id = request.args["emailid"]
        #print ("Json : {}".format(bill_details_json))

        return helper.handle_send_location(location_x, location_y, username, radius, count, email_id)



@app.route("/getitemlist")
def  get_item_list():
    app.logger.info("Received message for get_item_list : {} ".format(request.args))
    list_of_items = helper.handle_get_item_list()
    #return str(list_of_items)
    return str(",".join(list_of_items))

@app.route("/viewitemlist")
def  view_item_list():
    app.logger.info("Received message for get_item_list : {} ".format(request.args))
    list_of_items = helper.handle_get_item_list()
    #return str(list_of_items)
    return render_template('view_list.html',list = list_of_items if len(list_of_items)>0 else "Empty response")
