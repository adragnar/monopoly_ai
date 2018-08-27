import database

class Property_Manager() :

    #public
    def __init__(self):
        self.db = database.Database()

    def get_is_property_available(self, property_name):
        """Returns a specified property's purchase status
        Inputs: property_name(str)
        Outputs: yes or no(str)"""

        property_availability = self.db.read_value(property_name, "is_available_for_purchase")
        return property_availability

    def get_property_price(self):
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

    def get_owner(self, property_name):
        """Returns the owner of a specified property as a string
        Inputs: property_name(str)
        Outputs: name of the owner(str)"""

        property_owner = self.db.read_value(property_name, "owner")
        return property_owner

    def get_num_houses(self, property_name):
        """Returns the number of houses on a specific property as an integer
        Inputs: property_name(str)
        Outputs: num_houses(int)"""

        num_houses = self.db.read_value(property_name, "num_of_houses")
        return int(num_houses)

    def get_monopolies(self):
        """Returns the owner and colour of all monopolies on the board
        Inputs: None
        Outputs: Owner and colour in a list of lists where one list is the owner and another is colour"""

    def update_houses(self):
        """"""

    #private
    def read_property_deck(self, prop_id, info_type):
        pass
    def write_property_deck(self, prop_id, info_type, write_value):
        pass


if __name__ == "__main__":
    a = Property_Manager()
    b = a.get_num_houses("Baltic Ave.")
    print(b)
