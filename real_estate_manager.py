from property_manager import Property_Manager
from database import Database
import database_creator

class Real_Estate_Manager() :
    #public
    def __init__(self):
        self.available_houses = 33
        self.available_hotels = 12
        self.db = Database()
        self.a = Database()
        self.property_manager = Property_Manager()

    def build_real_estate(self, num_of_houses, prop_name, player_name): #Where is the player_name input stored?
        """Builds houses and hotels on houses with monopolies
            Inputs: number of houses being built(int), property name(str), player_name(str)
            Outputs: None"""
        if self.can_build(1):
            is_a_monopoly = self.a.read_value(prop_name, "is_a_monopoly")
            if is_a_monopoly == "yes":
                money_owned = int(self.a.read_value(player_name, "money"))
                property_build_cost = int(self.a.read_value(prop_name, "real_estate_price"))
                if money_owned > property_build_cost * num_of_houses:
                    old_num_of_houses = int(self.a.read_value(prop_name, "num_of_houses"))
                    final_num_of_houses = old_num_of_houses + num_of_houses
                    if final_num_of_houses <= 5:
                        if self.available_houses - num_of_houses > 0:
                            self.property_manager.update_houses(final_num_of_houses, prop_name) #num_of_houses and prop_name are given inputs. Where are those inputs stored?
                            self.available_houses -= num_of_houses
                            total_cost = money_owned - (property_build_cost * num_of_houses)
                            total_cost = str(total_cost)
                            self.a.write_value("money", total_cost, player_name)
                        else:
                            print("No more houses available")
                    else:
                        print("you have build the maximum amount of real-estate")

            else:
                print("hi")

        print(self.available_houses)


    def sell_real_estate(self, num_of_houses, prop_name, player_name):
        """Sell houses and hotels
            Inputs: number our houses being sold(int), property name(str), player_name(str)
            Outputs: None"""
        if player_name == self.db.read_value(prop_name, "owner"):
            if self.property_manager.get_num_houses(prop_name) > 0:
                if self.property_manager.get_num_houses(prop_name) >= num_of_houses:
                    #Work out refund anc make changes in database
                    money_owned = float(self.a.read_value(player_name, "money"))
                    property_build_cost = float(self.a.read_value(prop_name, "real_estate_price"))
                    refund = money_owned + ((property_build_cost / 2) * num_of_houses)
                    refund = str(refund)
                    self.a.write_value("money", refund, player_name)

                    #Subtract houses owned
                    new_num_houses = int(self.property_manager.get_num_houses(prop_name)) - num_of_houses
                    print("New num of houses = ", new_num_houses)
                    self.db.write_value("num_of_houses", str(new_num_houses), prop_name)
                else:
                    print("You are trying to sell more houses than you own!")
            else:
                print("You do not own any houses or hotels on that property!")
        else:
            print("You do not own that property!")


    #private
    def can_build(self, is_house):#indent expected?
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
    c = Real_Estate_Manager()
    print(c.sell_real_estate(3, "Baltic Ave.", "Player 2"))

