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

        player_counter = 0
        while 1:
            player_name = self.players[player_counter]
            print("The player name is", player_name)
            # Roll / jail
            double_roll_counter = 0
            jail_roll_counter = 0

            # Turn begins
            while 3 > double_roll_counter > -1:
                # Player's turn in jail
                if self.movement_manager.is_in_jail(player_name):
                    if int(self.db.read_value(player_name, "num_get_out_of_jail")) > 0:
                        use_get_out_of_jail_card = input("You have a get out of jail free card. Would you like to use it? (yes/no):")
                        if use_get_out_of_jail_card == "yes":
                            self.db.write_value("num_get_out_of_jail", "0", player_name)
                            roll = self.movement_manager.roll_dice(player_name)
                            roll = roll[0]
                            self.movement_manager.move(player_name, roll)
                            self.db.write_value("is_in_jail", "no", player_name)
                            jail_roll_counter = 0
                        else:
                            pass

                    else:
                        pay_for_roll = input("Would you like to pay $50 to get out of jail?")
                        if pay_for_roll == "yes":
                            # Give money to bank
                            self.rent_manager.pay_to_bank(player_name, 50, self.property_manager)
                            roll = self.movement_manager.roll_dice(player_name)
                            roll = roll[0]
                            self.movement_manager.move(player_name, roll)
                            self.db.write_value("is_in_jail", "no", player_name)
                            jail_roll_counter = 0
                        else:
                            print("Roll to get out of jail")
                            roll = self.movement_manager.roll_dice(player_name)
                            dice1 = roll[1]
                            dice2 = roll[2]
                            roll = roll[0]
                            if dice1 == dice2:
                                print("You have rolled out of jail")
                                self.movement_manager.move(player_name, roll)
                                self.db.write_value("is_in_jail", "no", player_name)
                                jail_roll_counter = 0
                                break
                            else:
                                # TODO Rolling out of jail (after 3 rolls you are automatically out),
                                print("You have not rolled out of jail")
                                jail_roll_counter += 1
                                if jail_roll_counter == 3:
                                    self.movement_manager.move(player_name, roll)
                                    self.db.write_value("is_in_jail", "no", player_name)
                                    jail_roll_counter = 0
                                break
                else:
                    pass

                # Roll
                roll = self.movement_manager.roll_dice(player_name)
                dice1 = roll[1]
                dice2 = roll[2]
                roll = roll[0]
                print("The roll is", roll)
                print("dice1 = ", dice1)
                print("dice2 = ", dice2)
                if dice1 == dice2:
                    double_roll_counter += 1
                else:
                    double_roll_counter = -2

                if double_roll_counter == 3:
                    self.movement_manager.go_to_jail(player_name)
                    break
                else:
                    pass

                # Player's turn in jail continued






                # Move/go to jail
                previous_location_value = self.movement_manager.get_current_location_value(player_name)
                self.movement_manager.move(player_name, roll)
                # Move to jail when land on 'Go to Jail' square
                print("prev = ", int(previous_location_value))
                print("current = ", int(self.movement_manager.get_current_location_value(player_name)))
                if int(previous_location_value) + roll == 30:
                    self.movement_manager.go_to_jail(player_name)
                    break
                else:
                    pass

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
                # Debugged

                if_trade = input("Was there a trade(yes/no)?: ")
                if if_trade == "yes":
                    opposing_player_name = input("What is the other player's name?: ")
                    num_current_properties = int(input("How many properties has " + player_name + " given?: "))
                    current_properties = []
                    for i in range(num_current_properties):
                        property = input("What property did the current player trade?: ")
                        current_properties.append(property)

                    num_opposing_properties = int(input("How many properties has the opposing player given?: "))
                    opposing_properties = []
                    for i in range(num_opposing_properties):
                        property = input("What property did the opposing player trade?: ")
                        opposing_properties.append(property)

                    current_money = int(input("How much money did the current player trade?: "))
                    opposing_money = int(input("How much money did the opposing player trade?: "))

                    self.real_estate_manager.trade(player_name, opposing_player_name, current_properties,
                                                   opposing_properties, current_money, opposing_money, self.property_manager)
                else:
                    pass
                # Debugged











            # End of turn. Transition into next turn
            print("OUT of all loops")
            double_roll_counter = 0
            player_counter += 1
            if player_counter == len(self.players):
                player_counter = 0
            else:
                pass
            # Debugged




if __name__ == "__main__":
    main = Main()
    main.main()
