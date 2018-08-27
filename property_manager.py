import database

class Property_Manager() :

    #public
    def __init__(self):
        self.db = database.Database()

    def get_is_property_available(self):
        pass
    def get_property_price(self, property_name):
        """Returns the price of a specified property.
        Input: property_name (string) - the name of the property
        Output: (int) the price to buy the property
        """
        property_price = self.db.read_value(property_name, "price")
        return int(property_price)

    def get_property_real_estate_price(self, property_name):
        """Returns cost of building house/hotel on a specified property.
        Input: property_name (string) - the name of the property
        Output: (int) the price to build house/hotel
        """
        real_estate_price = self.db.read_value(property_name, "real_estate_price")
        return int(real_estate_price)

    def get_property_real_estate_payout(self, property_name, num_pieces):
        """Returns rent of property with specified num of real estate built.
        Input: property_name (string) - the name of the property. num_pieces (int) num pieces of real estate on property
        Output: (int) the cost of rent
        """
        if (num_pieces == 0):
            rent = self.db.read_value(property_name, "rent")
            return int(rent)
        elif (num_pieces == 1) :
            rent = self.db.read_value(property_name, "price_for_one_house")
            return int(rent)
        elif (num_pieces == 2) :
            rent = self.db.read_value(property_name, "price_for_two_houses")
            return int(rent)
        elif (num_pieces == 3) :
            rent = self.db.read_value(property_name, "price_for_three_houses")
            return int(rent)
        elif (num_pieces == 4) :
            rent = self.db.read_value(property_name, "price_for_four_houses")
            return int(rent)
        elif (num_pieces == 5) :
            rent = self.db.read_value(property_name, "price_for_one_hotel")
            return int(rent)

    def get_owner(self):
        pass
    def get_num_houses(self):
        pass
    def get_monopolies(self):
        """"""
    def update_houses(self):
        """"""

    #private
    def read_property_deck(self, prop_id, info_type):
        pass
    def write_property_deck(self, prop_id, info_type, write_value):
        pass