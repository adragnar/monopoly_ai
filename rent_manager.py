from database import Database
import database_creator
import property_manager

class RentManager:

    # public
    def __init__(self):
        self.dbb = database_creator.get_database()
        self.db = Database()

    def check_if_rent_owed(self, current_player, property_manager, movement_manager):
        """Check to see if a player needs to pay rent
        Inputs: the name of the player whose turn it is (str)
        Outputs: None
        :return: True if rent is owed and False if rent is not owed
        """
        current_prop_name = property_manager.get_current_property_name(current_player, movement_manager)
        current_prop_owner = property_manager.get_current_property_owner(current_player)
        if current_prop_owner != current_player and current_prop_owner is not None:
            if not self.check_if_mortgaged(current_prop_name):
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



    def check_if_and_num_houses(self, prop_name):
        """Will return the number of houses on a specific property
        Inputs: Property name(str)
        Outputs: # of houses on the property(str)"""
        if_houses = self.db.read_value(prop_name, "num_of_houses")
        return if_houses

    def pay_rent(self, current_player, property_manager, movement_manager):
        """
        It will pay the rent. It finds all of the information. All you need to pass in is the current player's name
        :param current_player: name of the current player
        :return: None
        """
        property_name = property_manager.get_current_property_name(current_player, movement_manager)
        print("Property name = ", property_name)
        receiving_player = property_manager.get_current_property_owner(current_player, movement_manager)
        real_estate_rent = 0

        places_where_no_pay_rent = ["Community Chest", "Chance", "Visiting Jail", "Free Parking", "Go To Jail", "Go"]
        railroads = ["Reading Railroad", "Pennsylvania Railroad", "B. & O. Railroad", "Short Line"]

        if property_manager.get_current_property_owner(current_player, movement_manager) == current_player:
            print("1")
            pass
        elif property_manager.get_current_property_name(current_player, movement_manager) == "Income Tax" or property_manager.get_current_property_name(current_player, movement_manager) == "Luxury Tax":
            if property_manager.get_current_property_name(current_player, movement_manager) == "Income Tax":
                current_player_balance = property_manager.get_balance(current_player)
                property_rent = int(self.db.read_value("Income Tax", "rent"))
                new_current_player_balance = current_player_balance - property_rent
                self.db.write_value("money", new_current_player_balance, current_player)
            elif property_manager.get_current_property_name(current_player, movement_manager) == "Luxury Tax":
                current_player_balance = property_manager.get_balance(current_player)
                property_rent = int(self.db.read_value("Luxury Tax", "rent"))
                new_current_player_balance = current_player_balance - property_rent
                self.db.write_value("money", new_current_player_balance, current_player)
        elif property_manager.get_current_property_name(current_player, movement_manager) == "Electric Company" or property_manager.get_current_property_name(current_player, movement_manager) == "Water Works":
            print("In utility loop")
            if property_manager.get_other_monopolies_owner("utility")[0][0] == receiving_player and property_manager.get_other_monopolies_owner("utility")[1][0] == receiving_player:
                # Monopoly rent
                current_player_balance = property_manager.get_balance(current_player)
                receiving_player_balance = property_manager.get_balance(receiving_player)

                roll = movement_manager.roll
                print("roll in loop is", roll)

                property_rent = roll * 10

                new_current_player_balance = current_player_balance - property_rent
                new_receiving_player_balance = receiving_player_balance + property_rent

                # Money loss
                self.db.write_value("money", new_current_player_balance, current_player)
                # Money gain
                self.db.write_value("money", new_receiving_player_balance, receiving_player)
            else:
                # Non monopoly rent
                current_player_balance = property_manager.get_balance(current_player)
                receiving_player_balance = property_manager.get_balance(receiving_player)

                roll = movement_manager.roll
                print("roll in loop is", roll)

                property_rent = roll * 4

                new_current_player_balance = current_player_balance - property_rent
                new_receiving_player_balance = receiving_player_balance + property_rent

                # Money loss
                self.db.write_value("money", new_current_player_balance, current_player)
                # Money gain
                self.db.write_value("money", new_receiving_player_balance, receiving_player)

        elif property_manager.get_current_property_owner(current_player, movement_manager) is None or property_manager.get_current_property_owner(current_player, movement_manager) == "":
            print("3")
            pass
        elif property_manager.get_current_property_name(current_player, movement_manager) in places_where_no_pay_rent:
            print("4")
            pass
        else:
            print("LOOK HEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
            if self.check_if_monopoly(property_name):
                print("yooooooo")
                num_houses = property_manager.get_num_houses(property_name)
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
                property_rent = (int(self.db.read_value(property_name, "rent")) * 2) + real_estate_rent

                print("Property rent = ", property_rent)
                current_player_balance = property_manager.get_balance(current_player)
                receiving_player_balance = property_manager.get_balance(receiving_player)
                new_current_player_balance = current_player_balance - property_rent
                new_receiving_player_balance = receiving_player_balance + property_rent
                print("New receiving Player Balance = ", new_receiving_player_balance)
                print("New current player balance = ", new_current_player_balance)
                # Money loss
                self.db.write_value("money", new_current_player_balance, current_player)
                # Money gain
                self.db.write_value("money", new_receiving_player_balance, receiving_player)
            elif property_name in railroads:
                print("yelll")
                print("hi")
                print("receving player = ", receiving_player)
                num_railroads_owned = property_manager.get_num_railroads_owned(receiving_player)
                if num_railroads_owned == 1:
                    property_rent = int(self.db.read_value(property_name, "rent_for_one_railroad"))
                elif num_railroads_owned == 2:
                    property_rent = int(self.db.read_value(property_name, "rent_for_two_railroads"))
                elif num_railroads_owned == 3:
                    property_rent = int(self.db.read_value(property_name, "rent_for_three_railroads"))
                elif num_railroads_owned == 4:
                    property_rent = int(self.db.read_value(property_name, "rent_for_four_railroads"))

                print("Property rent = ", property_rent)
                current_player_balance = property_manager.get_balance(current_player)
                receiving_player_balance = property_manager.get_balance(receiving_player)
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
                current_player_balance = property_manager.get_balance(current_player)
                receiving_player_balance = property_manager.get_balance(receiving_player)
                new_current_player_balance = current_player_balance - property_rent
                new_receiving_player_balance = receiving_player_balance + property_rent
                print("New receiving Player Balance = ", new_receiving_player_balance)
                print("New current player balance = ", new_current_player_balance)
                #Money loss
                self.db.write_value("money", new_current_player_balance, current_player)
                #Money gain
                self.db.write_value("money", new_receiving_player_balance, receiving_player)
                print("yaaaaa")



    #Private
    def pay_to_bank(self, player_name, amount, property_manager):
        """
        Give money to bank
        :param player_name: Name of player
        :param amount: amount of money that is given(int)
        :param property_manager: PropertyManager() class
        :return: None
        """
        current_player_balance = property_manager.get_balance(player_name)
        new_current_player_balance = current_player_balance - amount
        self.db.write_value("money", new_current_player_balance, player_name)

    def pay_to_other_player(self, current_player, receiving_player, money_given, property_manager):
        """
        Pay other players money
        :param current_player: Giving player name
        :param receiving_player: Receiving money player name
        :param money_given: amount of money given (int)
        :param property_manager: PropertyManager() clas
        :return: None
        """
        current_player_balance = property_manager.get_balance(current_player)
        receiving_player_balance = property_manager.get_balance(receiving_player)
        new_current_player_balance = current_player_balance - money_given
        new_receiving_player_balance = receiving_player_balance + money_given

        self.db.write_value("money", new_current_player_balance, current_player)
        self.db.write_value("money", new_receiving_player_balance, receiving_player)

    '''
    def get_roll(self, player_name):
        """
        Gets a player's roll
        :param player_name: Name of player
        :return: int of the player's roll
        """
        roll = self.db.read_value(player_name, "roll")
        return roll
    '''




if __name__ == "__main__":
    b = RentManager()
    prop_manager = property_manager.PropertyManager()
    b.pay_to_other_player("Player 1", "Player 2", 300, prop_manager)
