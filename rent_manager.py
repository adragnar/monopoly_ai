from database import Database

class Rent_Manager() :



    #public
    def __init__(self):
        self.a = Database()

    def check_if_rent_owed(self, owing_player_name, receiving_player_name):
        None

    def check_if_monopoly(self, property_id):
        None
    def check_if_houses(self, prop_name):
        """Will return the number of houses on a specific property
        Inputs: Property name(str)
        Outputs: # of houses on the property(str)"""
        if_houses = self.a.read_value(prop_name, "num_of_houses")
        return if_houses

    def pay_rent(self, sender_id, receiver_id, amount):
        """"""

if __name__ == "__main__":
    b = Rent_Manager()
    b.check_if_houses("Baltic Ave.")