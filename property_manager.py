import database_creator
import database

class property_manager() :

    #public
    def __init__(self):
        self.db = database()

    def get_is_property_available(self):

    def get_property_price(self):

    def get_property_real_estate_price(self):

    def get_property_real_estate_payout(self, num_pieces):

    def get_owner(self):

    def get_num_houses(self):

    def get_monopolies(self):
        """"""
    def update_houses(self):
        """"""

    #private
    def read_property_deck(self, prop_id, info_type):

    def write_property_deck(self, prop_id, info_type, write_value):