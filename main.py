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
            # Roll
            roll = int(input("Enter " + player_name + "'s roll: "))
            # Move
            self.movement_manager.move(player_name, roll)
            # Check to see if it can be purchased
            prop_name = self.property_manager.get_current_property_name(player_name)
            if self.property_manager.get_is_property_available(prop_name) == "yes":
                purchase = input("Was the property purchased? (yes/no):")
                #If the property was purchased
                if purchase == "yes":
                    self.property_manager.buy_property(player_name)
                else:
                    print("The property was not purchased")
            else:
                # If the property is not available pay rent (this function takes care of all rent/tax stuff).
                self.rent_manager.pay_rent(player_name)
                if self.property_manager.get_balance(player_name) < 0:
                    print(player_name + " is bankrupt")
                    self.players.pop(player_counter)
                else:
                    pass

            # Post property buying / rent (Building)




if __name__ == "__main__":
    main = Main()
    main.main()