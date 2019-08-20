import database
import property_manager
import real_estate_manager
import  rent_manager
import movement_manager

class Main:

    def __init__(self):
        self.db = database.Database()
        self.property_manager = property_manager.PropertyManager()
        self.real_estate_manager = real_estate_manager.RealEstateManager()
        self.rent_manager = rent_manager.RentManager()
        self.movement_manager = movement_manager.MovementManager()

        self.num_players = 0
        self.players = []

    def main(self):
        self.num_players = int(input("How many players total are in the game (including me)?: "))
        for i in range(1, self.num_players + 1):
            self.players.append("Player " + str(i))


        while 1:
            player_counter = 0
            player_name = self.players[player_counter]
            print("The player name is", player_name)
            # Roll
            roll = self.movement_manager.roll_dice(player_name)
            print("The roll is", roll)
            # Move
            self.movement_manager.move(player_name, roll)
            # Check to see if it can be purchased
            prop_name = self.property_manager.get_current_property_name(player_name, self.movement_manager)
            if self.property_manager.get_is_property_available(prop_name) == "yes":
                purchase = input("Was the property purchased? (yes/no):")
                #If the property was purchased
                if purchase == "yes":
                    self.property_manager.buy_property(player_name, self.movement_manager)
                else:
                    print("The property was not purchased")
            else:
                # VERY IMPORTANT!!!!!!!!!!!!!!!!! SETS UNDOCUMENTED MONOPOLIES TO "YES"
                self.property_manager.get_monopolies()
                # If the property is not available pay rent (this function takes care of all rent/tax stuff).
                self.rent_manager.pay_rent(player_name, self.property_manager, self.movement_manager)
                if self.property_manager.get_balance(player_name) < 0:
                    print(player_name + " is bankrupt")
                    self.players.pop(player_counter)
                else:
                    pass
            #Debugged



            # TODO Deal with Chance and Community Chest Cards
            # TODO Deal with double rolls
            # TODO Deal with Trading

            # Post property buying / rent (Building)
            # Real estate buying/selling
            real_estate_bought = input("Was any real estate bought? (yes/no): ")
            if real_estate_bought == "yes":
                num_properties = input("How many properties was real estate bought on?: ")
                for i in range(int(num_properties)):
                    property_name = input("What's the property's name?: ")
                    num_real_estate = int(input("How much real estate was bought?: "))
                    current_balance = self.property_manager.get_balance(player_name)
                    real_estate_cost = int(self.db.read_value(property_name, "real_estate_price")) * num_real_estate
                    new_balance = current_balance - int(real_estate_cost)

                    new_num_real_estate = int(self.rent_manager.check_if_and_num_houses(property_name)) + num_real_estate

                    self.db.write_value("num_of_houses", new_num_real_estate, property_name)
                    self.db.write_value("money", new_balance, player_name)
            else:
                pass

            real_estate_sold = input("Was any real estate sold? (yes/no): ")
            if real_estate_sold == "yes":
                num_properties = input("How many properties was real estate sold on?: ")
                for i in range(int(num_properties)):
                    property_name = input("What's the property's name?: ")
                    num_real_estate = int(input("How much real estate was sold?: "))
                    current_balance = self.property_manager.get_balance(player_name)
                    real_estate_cost = int(int(self.db.read_value(property_name, "real_estate_price")) / 2 * num_real_estate)
                    new_balance = current_balance + int(real_estate_cost)

                    new_num_real_estate = int(self.rent_manager.check_if_and_num_houses(property_name)) - num_real_estate

                    self.db.write_value("num_of_houses", new_num_real_estate, property_name)
                    self.db.write_value("money", new_balance, player_name)
            else:
                pass





if __name__ == "__main__":
    main = Main()
    main.main()
