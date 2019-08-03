from database import Database
import database_creator
import property_manager


class RentManager:

    #public
    def __init__(self):
        self.dbb = database_creator.get_database()
        self.db = Database()
        self.property_manager = property_manager.PropertyManager()

    def check_if_rent_owed(self, current_player):
        """Check to see if a player needs to pay rent
        Inputs: the name of the player whose turn it is (str)
        Outputs: None
        :return: True if rent is owed and False if rent is not owed
        """
        current_prop_name = self.get_current_property_name(current_player)
        current_prop_owner = self.get_current_property_owner(current_player)
        if current_prop_owner != current_player and current_prop_owner != None:
            if self.check_if_mortgaged(current_prop_name) == False:
                print("yes")
                return True
            else:
                return False
        else:
            print("no")
            return False

    def check_if_monopoly(self, property_name):
        """
        Checks to see if a property is in a monopoly
        :param property_name: name of a property that you are checking to see if its a monopoly
        :return: True if the property is a monopoly and False if it isn't
        """
        if self.db.read_value(property_name, "is_a_monopoly") == "yes":
            return True
        else:
            return False

    def check_if_mortgaged(self, property_name):
        """
        Checks to see if a property is mortgaged
        :param property_name: Name of property (str)
        :return: True if the property is mortgaged and False if it's not
        """
        if self.db.read_value(property_name, "is_mortgaged") == "yes":
            return True
        else:
            return False

    def get_balance(self, player_name):
        """
        Return's a player's total monety
        :param player_name: Name of the player you are getting the balance from (str)
        :return: The amount of money they have (int)
        """
        balance = int(self.db.read_value(player_name, "money"))
        return balance

    def check_if_and_num_houses(self, prop_name):
        """Will return the number of houses on a specific property
        Inputs: Property name(str)
        Outputs: # of houses on the property(str)"""
        if_houses = self.db.read_value(prop_name, "num_of_houses")
        return if_houses

    def pay_rent(self, current_player):
        """
        It will pay the rent. It finds all of the information. All you need to pass in is the current player's name
        :param current_player: name of the current player
        :return: None
        """
        property_name = self.get_current_property_name(current_player)
        receiving_player = self.get_current_property_owner(current_player)
        if self.check_if_monopoly(property_name):
            num_houses = self.property_manager.get_num_houses(property_name)
            if num_houses == 0:
                real_estate_rent = 0
            elif num_houses == 1:
                real_estate_rent = int(self.db.read_value(property_name, "price_for_one_house"))
            elif num_houses == 2:
                real_estate_rent = int(self.db.read_value(property_name, "price_for_two_houses"))
            elif num_houses == 3:
                real_estate_rent = int(self.db.read_value(property_name, "price_for_three_houses"))
            elif num_houses == 4:
                real_estate_rent = int(self.db.read_value(property_name, "price_for_four_houses"))
            elif num_houses == 5:
                real_estate_rent = int(self.db.read_value(property_name, "price_for_one_hotel"))
            else:
                pass
            print("num houses = ", num_houses)
            print("real estate rent = ", real_estate_rent)
            property_rent = (int(self.db.read_value(property_name, "rent")) * 2) + real_estate_rent

            print("Property rent = ", property_rent)
            current_player_balance = self.get_balance(current_player)
            receiving_player_balance = self.get_balance(receiving_player)
            new_current_player_balance = current_player_balance - property_rent
            new_receiving_player_balance = receiving_player_balance + property_rent
            print("New receiving Player Balance = ", new_receiving_player_balance)
            print("New current player balance = ", new_current_player_balance)
            # Money loss
            self.db.write_value("money", new_current_player_balance, current_player)
            # Money gain
            self.db.write_value("money", new_receiving_player_balance, receiving_player)
        else:
            property_rent = int(self.db.read_value(property_name, "rent"))
            print("Property rent = ", property_rent)
            current_player_balance = self.get_balance(current_player)
            receiving_player_balance = self.get_balance(receiving_player)
            new_current_player_balance = current_player_balance - property_rent
            new_receiving_player_balance = receiving_player_balance + property_rent
            print("New receiving Player Balance = ", new_receiving_player_balance)
            print("New current player balance = ", new_current_player_balance)
            #Money loss
            self.db.write_value("money", new_current_player_balance, current_player)
            #Money gain
            self.db.write_value("money", new_receiving_player_balance, receiving_player)


    #Private
    def get_current_location_value(self, player_name):
        """
        Gets a players numerical location on the board (str)
        :param player_name: Name of player (str)
        :return: a player's numerical location on the board (str)
        """
        current_location_value = self.db.read_value(player_name, "spot_on_board")
        return current_location_value

    def get_current_property_name(self, player_name):
        """
        Gets the name of the property a player is currently on
        :param player_name: name of the player
        :return: The name of the property a player is currently on (str)
        """
        current_location_num = self.get_current_location_value(player_name)
        current_property_name = self.db.specific_read_value(current_location_num, "board_position", "name")
        return current_property_name

    def get_current_property_owner(self, player_name):
        """
        Gets the owner of the property a player is currently on
        :param player_name: Name of the player (str)
        :return: The owner of a property the player is currently on (str)
        """
        current_location_num = self.get_current_location_value(player_name)
        current_prop_owner = self.db.specific_read_value(current_location_num, "board_position", "owner")
        return current_prop_owner



if __name__ == "__main__":
    b = RentManager()
    print(b.pay_rent("Player 2"))