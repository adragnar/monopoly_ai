from database import Database

class RealEstateManager:

    # public
    def __init__(self):
        self.available_houses = 32
        self.available_hotels = 12
        self.db = Database()

    def build_real_estate(self, num_of_houses, prop_name, player_name, property_manager):  # Where is the player_name input stored?
        """Builds houses and hotels on houses with monopolies
            Inputs: number of houses being built(int), property name(str), player_name(str)
            Outputs: None"""
        if self.can_build(1):
            is_a_monopoly = self.db.read_value(prop_name, "is_a_monopoly")
            if is_a_monopoly == "yes":
                money_owned = int(self.db.read_value(player_name, "money"))
                property_build_cost = int(self.db.read_value(prop_name, "real_estate_price"))
                if money_owned > property_build_cost * num_of_houses:
                    old_num_of_houses = int(self.db.read_value(prop_name, "num_of_houses"))
                    final_num_of_houses = old_num_of_houses + num_of_houses
                    if final_num_of_houses <= 5:
                        if self.available_houses - num_of_houses > 0:
                            property_manager.update_houses(final_num_of_houses,
                                                                prop_name)  # num_of_houses and prop_name are given inputs. Where are those inputs stored?
                            total_cost = money_owned - (property_build_cost * num_of_houses)
                            total_cost = str(total_cost)
                            self.db.write_value("money", total_cost, player_name)
                        else:
                            print("No more houses available")
                    else:
                        print("you have build the maximum amount of real-estate")

            else:
                print("hi")

        print(self.available_houses)

    def sell_real_estate(self, num_of_houses, prop_name, player_name, property_manager):
        """Sell houses and hotels
            Inputs: number our houses being sold(int), property name(str), player_name(str)
            Outputs: None"""
        if player_name == self.db.read_value(prop_name, "owner"):
            if property_manager.get_num_houses(prop_name) > 0:
                if property_manager.get_num_houses(prop_name) >= num_of_houses:
                    # Work out refund anc make changes in database
                    money_owned = float(self.db.read_value(player_name, "money"))
                    property_build_cost = float(self.db.read_value(prop_name, "real_estate_price"))
                    refund = money_owned + ((property_build_cost / 2) * num_of_houses)
                    refund = str(refund)
                    self.db.write_value("money", refund, player_name)

                    # Subtract houses owned
                    new_num_houses = int(property_manager.get_num_houses(prop_name)) - num_of_houses
                    print("New num of houses = ", new_num_houses)
                    self.db.write_value("num_of_houses", str(new_num_houses), prop_name)
                else:
                    print("You are trying to sell more houses than you own!")
            else:
                print("You do not own any houses or hotels on that property!")
        else:
            print("You do not own that property!")

    def trade(self, current_player_name, opposing_player_name, current_properties, opposing_properties, current_money,
              opposing_money, property_manager):
        """
        Trades stuff
        :param current_player_name: Name of player whose turn it is
        :param opposing_player_name: Name of player the current player is trading with
        :param current_properties: list of all properties the current player is trading (list)
        :param opposing_properties: List of all properties the other player is trading (list)
        :param current_money: The amount of money the current player is giving the other player (int)
        :param opposing_money: The amount of money the other player is giving the current player (int)
        #:param current_cards: list of all community chest or chance cards the current player is giving (list)
        #:param opposing_cards: List of all community chest or chance cards the other player is giving the current player (list)
        :return: None
        """
        for i in current_properties:
            self.db.write_value("owner", opposing_player_name, i)

        for i in opposing_properties:
            self.db.write_value("owner", current_player_name, i)

        current_player_balance = int(self.db.read_value(current_player_name, "money"))
        new_current_player_balance = current_player_balance + opposing_money - current_money
        self.db.write_value("money", new_current_player_balance, current_player_name)

        opposing_player_balance = int(self.db.read_value(opposing_player_name, "money"))
        new_opposing_player_balance = opposing_player_balance + int(current_money) - opposing_money
        self.db.write_value("money", new_opposing_player_balance, opposing_player_name)

        property_manager.get_monopolies()
        '''
        for i in current_cards:
            self.db.write_value("owner", opposing_player_name, i)

        for i in opposing_cards:
            self.db.write_value("owner", current_player_name, i)
        '''


    def trade_in(self):
        pass


    # private
    def can_build(self, is_house):  # indent expected?
        """Determines whether it is possible to build a house or hotel.
         Input: is_house, bool that is 1 if want to build house, 0 if want to build hotel
         Return: bool indicating whether can build
         Class_vars_mod_: none
         """
        if is_house == 1:
            if self.available_houses >= 1:
                return True
            else:
                return False
        else:
            if self.available_hotels >= 1:
                return True
            else:
                return False


if __name__ == "__main__":
    c = RealEstateManager()
    print(c.trade("Player 2", "Player 3", ["Baltic Ave.", "Oriental Ave."], ["Mediterranean Ave.", "Vermont Ave."], 125, 150))
