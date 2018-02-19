

class Offer():
    location_x = 0.0
    location_y = 0.0
    place = "SamplePlace"
    item = "SampleItem"
    discount = 5

    def __init__(self, location_x, location_y, place, item, discount):
        self.location_x = location_x
        self.location_y = location_y
        self.place = place
        self.item = item
        self.discount = discount

    # For string representation
    def __repr__(self):
        return "{} at {}% discount at {} ({},{})".format(self.item, self.discount, self.place, self.location_x, self.location_y)


def get_queue_for_user(username):

    # Sample offers
    sample_offer = Offer("20.2","54.0","Big Bazaar","Milk",5)
    list_of_offers_for_user = [str(sample_offer)]

    return list_of_offers_for_user
