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
        self.num_npc = 0

    def main(self):
        #print(self.property_manager.getNumEmptyHouses("orange"))
        #print(self.property_manager.get_monopolies())
        self.num_players = int(input("How many players total are in the game (including me)?: "))
        for i in range(1, self.num_players + 1):
            self.players.append("Player " + str(i))

        # Add the NPCs
        self.num_npc = int(input("How many NPCs total are in the game?: "))
        for i in range(1, self.num_npc +1):
            self.players.append("NPC " + str(i))


        turnNum = 1
        player_counter = 0
        while 1:
            print("Player counter =", player_counter)
            print(self.players)
            player_name = self.players[player_counter]
            print("The player name is", player_name)
            # Roll / jail

            # Turn begins
            while 3 <= self.movement_manager.getNumDoubleRolls(player_name):
                print("here")
                # If they land on Chance or Community Chest spot
                community_chest_spots = ["2", "17", "33"]
                chance_spots = ["7", "22", "36"]
                if self.movement_manager.get_current_location_value(player_name) in community_chest_spots:
                    specific_card = input("Enter the first two words of your community chest card (including capital letters): ")
                    if specific_card in ["Bank error", "From sale", "Holiday fund", "Income tax", "It is", "Life insurance", "Receive $25", "You have", "You inherit"]:
                        money = int(self.db.read_value(specific_card, "community_chest_money_gained"))
                        self.rent_manager.gain_money_from_bank(player_name, money)
                    else:
                        pass












                # Player's turn in jail
                if self.movement_manager.is_in_jail(player_name):
                    if int(self.db.read_value(player_name, "num_get_out_of_jail")) > 0:
                        # NPC handling if in jail
                        if player_name[0] == "N":
                            if self.movement_manager.check_get_out_cards(player_name) == True:
                                self.movement_manager.leave_jail(player_name)
                                self.movement_manager.roll_dice_in_jail(player_name)
                                self.movement_manager.resetJailRolls(player_name)
                            else:
                                pass
                        else:
                            use_get_out_of_jail_card = input("You have a get out of jail free card. Would you like to use it? (yes/no):")
                            if use_get_out_of_jail_card == "yes":
                                self.movement_manager.leave_jail(player_name)
                                self.movement_manager.roll_dice_in_jail(player_name)
                                self.movement_manager.resetJailRolls(player_name)
                            else:
                                pass

                    else:
                        #NPC Handling
                        if player_name[0] == "N":
                            if self.property_manager.get_balance(player_name) >= 150:
                                self.rent_manager.pay_to_bank(player_name, 50, self.property_manager)
                                self.movement_manager.roll_dice_in_jail(player_name)
                                self.movement_manager.leave_jail(player_name)
                                self.movement_manager.resetJailRolls(player_name)
                            else:
                                print("Roll to get out of jail")
                                roll = self.movement_manager.npcDiceRoll()
                                dice1 = roll[1]
                                dice2 = roll[2]
                                roll = roll[0]
                                if dice1 == dice2:
                                    print("You have rolled out of jail")
                                    self.movement_manager.move(player_name, roll)
                                    self.movement_manager.leave_jail(player_name)
                                    self.movement_manager.resetJailRolls(player_name)
                                    break
                                else:
                                    # TODO Rolling out of jail (after 3 rolls you are automatically out),
                                    print("You have not rolled out of jail")
                                    self.movement_manager.incrementJailRolls(player_name)
                                    if self.movement_manager.getNumJailRolls(player_name) == 3:
                                        self.movement_manager.move(player_name, roll)
                                        self.movement_manager.leave_jail(player_name)
                                        self.movement_manager.resetJailRolls(player_name)
                                    break
                        else:
                            pay_for_roll = input("Would you like to pay $50 to get out of jail?")
                        if pay_for_roll == "yes":
                            # Give money to bank
                            self.rent_manager.pay_to_bank(player_name, 50, self.property_manager)
                            self.movement_manager.roll_dice_in_jail(player_name)
                            self.movement_manager.leave_jail(player_name)
                            self.movement_manager.resetJailRolls(player_name)
                        else:
                            print("Roll to get out of jail")
                            roll = self.movement_manager.roll_dice(player_name)
                            dice1 = roll[1]
                            dice2 = roll[2]
                            roll = roll[0]
                            if dice1 == dice2:
                                print("You have rolled out of jail")
                                self.movement_manager.move(player_name, roll)
                                self.movement_manager.leave_jail(player_name)
                                self.movement_manager.resetJailRolls(player_name)
                                break
                            else:
                                # TODO Rolling out of jail (after 3 rolls you are automatically out),
                                print("You have not rolled out of jail")
                                self.movement_manager.incrementJailRolls(player_name)
                                if self.movement_manager.getNumJailRolls(player_name) == 3:
                                    self.movement_manager.move(player_name, roll)
                                    self.movement_manager.leave_jail(player_name)
                                    self.movement_manager.resetJailRolls(player_name)
                                break
                else:
                    pass

            # Handle NPC movement on normal rolls
            if player_name[0] == "N":
                print("NPC rolling")
                roll = self.movement_manager.npcDiceRoll()
                dice1 = roll[1]
                dice2 = roll[2]
                roll = roll[0]
            else:
                # Roll
                print("regular rolling")
                roll = self.movement_manager.roll_dice(player_name)
                dice1 = roll[1]
                dice2 = roll[2]
                roll = roll[0]

            print("The roll is", roll)
            print("dice1 = ", dice1)
            print("dice2 = ", dice2)
            if dice1 == dice2:
                self.movement_manager.incrementDoubleRolls(player_name)
            else:
                self.movement_manager.resetNumDoubleRolls(player_name)

            if self.movement_manager.getNumDoubleRolls(player_name) == 3:
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
                if player_name[0] == "N":
                    # Logic for NPC property buying
                    # IF there are no monopolies currently on the board
                    if self.property_manager.get_monopolies() is None:
                        # If NPC can afford property
                        if self.property_manager.get_balance(player_name) > self.property_manager.get_property_price(prop_name):
                            self.property_manager.buy_property(player_name, self.movement_manager)
                            print("Property purchased")
                        else:
                            print("Property not purchased")
                    else:
                        # If there are monopolies on the board and the player has $300+
                        if self.property_manager.get_balance(player_name) >= 300:
                            self.property_manager.buy_property(player_name, self.movement_manager)
                            print("Property purchased")
                        else:
                            print("Property not purchased")
                else:
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
                    # Handle Bankruptcy for NPC (I.E. Selling houses if possible)
                    if player_name[0] == "N":
                        monopolies = self.property_manager.get_monopolies()
                        colours = []

                        for i in monopolies:
                            if player_name == i[0]:
                                colours.append(i[1])

                        for i in colours:
                            numIndividualEmptyHouseSlots = self.property_manager.getNumEmptyHouses(i)
                            properties = self.property_manager.getProperties(i)
                            for j in range(len(numIndividualEmptyHouseSlots)):
                                if numIndividualEmptyHouseSlots[j] < 5:
                                    self.real_estate_manager.sell_real_estate(1, properties[j], player_name, self.property_manager)
                                if self.property_manager.get_balance(player_name) >= 0:
                                    break
                            if self.property_manager.get_balance(player_name) >= 0:
                                break
                        if self.property_manager.get_balance(player_name) < 0:
                            print(player_name + " is bankrupt")
                            self.players.pop(player_counter)
                    else:
                        print(player_name + " is bankrupt")
                        self.players.pop(player_counter)
                else:
                    pass
            #Debugged


            # TODO Deal with Chance and Community Chest Cards

            # Post property buying / rent (Building)
            # Real estate buying/selling
            if player_name[0] == "N":
                # If they have a monopoly, if they can build, build as much as possible. If there are other monopolies, save a bit of money
                monopolies = self.property_manager.get_monopolies()
                colours = []
                prices = []
                for i in monopolies:
                    if player_name == i[0]:
                        if i[1] not in colours:
                            colours.append(i[1])


                # Query for properties of the colours retrieved from the get_monopolies() function
                for i in colours:
                    if i == "purple":
                        prices.append(int(self.db.read_value("Mediterranean Ave.", "real_estate_price")))
                    elif i == "grey":
                        prices.append(int(self.db.read_value("Oriental Ave.", "real_estate_price")))
                    elif i == "pink":
                        prices.append(int(self.db.read_value("St. Charles Place", "real_estate_price")))
                    elif i == "orange":
                        prices.append(int(self.db.read_value("St. James Place", "real_estate_price")))
                    elif i == "red":
                        prices.append(int(self.db.read_value("Kentucky Ave.", "real_estate_price")))
                    elif i == "yellow":
                        prices.append(int(self.db.read_value("Atlantic Ave.", "real_estate_price")))
                    elif i == "green":
                        prices.append(int(self.db.read_value("Pacific Ave.", "real_estate_price")))
                    elif i == "blue":
                        prices.append(int(self.db.read_value("Park Place", "real_estate_price")))
                    else:
                        pass

                print("colours = ",colours)
                print("prices = ", prices)


                for i in range(len(colours)):
                    if self.property_manager.get_balance(player_name) > prices[i]:
                        numPotentialBuyingHouses = self.property_manager.get_balance(player_name) // prices[i]
                        numIndividualEmptyHouseSlots = self.property_manager.getNumEmptyHouses(colours[i])
                        if len(numIndividualEmptyHouseSlots) == 3:
                            print("numIndividualEmptyHouseSlots = ", numIndividualEmptyHouseSlots)
                            numSumEmptyHouseSlots = numIndividualEmptyHouseSlots[0] + numIndividualEmptyHouseSlots[1] + numIndividualEmptyHouseSlots[2]
                        elif len(numIndividualEmptyHouseSlots) == 2:
                            print("numIndividualEmptyHouseSlots = ", numIndividualEmptyHouseSlots)
                            numSumEmptyHouseSlots = numIndividualEmptyHouseSlots[0] + numIndividualEmptyHouseSlots[1] + numIndividualEmptyHouseSlots[2]

                        # What I can buy after related to everything
                        potentialHouses = 0
                        potentialHotels = 0
                        # If houses are being built
                        if numSumEmptyHouseSlots > 3:
                            if numPotentialBuyingHouses >= 1:
                                if numPotentialBuyingHouses <= self.real_estate_manager.available_houses:
                                    # Represents all potential real estate (houses and hotels combined here)
                                    potentialHouses = numPotentialBuyingHouses
                                elif numPotentialBuyingHouses > self.real_estate_manager.available_houses:
                                    potentialHouses = self.real_estate_manager.available_houses
                        else:
                            # Build just hotels
                            print("Just hotels")
                            if numPotentialBuyingHouses >= 1:
                                if numPotentialBuyingHouses <= self.real_estate_manager.available_hotels:
                                    potentialHotels = numPotentialBuyingHouses
                                elif numPotentialBuyingHouses > self.real_estate_manager.available_hotels:
                                    potentialHotels = self.real_estate_manager.available_hotels


                        if potentialHouses <= numSumEmptyHouseSlots - 3 or numSumEmptyHouseSlots - potentialHouses >= 3:
                            # All "potentialHouses" are houses
                            pass
                        else:
                            print("Getting houses and hotels")
                            print("all real estate = ", potentialHouses)
                            print("numSumEmptyHOuseSLots = ", numSumEmptyHouseSlots)
                            potentialHotels = potentialHouses - numSumEmptyHouseSlots + 3
                            print("potential hotels = ", potentialHotels)
                            potentialHouses = potentialHouses - potentialHotels + 3


                        # Get the order of the houses that are going to be built
                        if potentialHouses > 0 :
                            propOrder = sorted(numIndividualEmptyHouseSlots, reverse=True)
                            propNameOrder = []

                            if len(numIndividualEmptyHouseSlots) == 2:
                                print("size 2")
                                firstPropNum = numIndividualEmptyHouseSlots[0]
                                secondPropNum = numIndividualEmptyHouseSlots[1]
                                thirdPropNum = -1
                                props = [firstPropNum, secondPropNum, thirdPropNum]

                                potentialProps = ["first", "second"]
                                print("propOrder = ", propOrder)
                                for i in propOrder:
                                    if i == firstPropNum:
                                        if "first" in potentialProps:
                                            propNameOrder.append("first")
                                        else:
                                            propNameOrder.append("second")
                                    elif i == secondPropNum:
                                        if "second" in potentialProps:
                                            propNameOrder.append("second")
                                        else:
                                            propNameOrder.append("first")

                            elif len(numIndividualEmptyHouseSlots) == 3:
                                print("size 3")
                                firstPropNum = numIndividualEmptyHouseSlots[0]
                                secondPropNum = numIndividualEmptyHouseSlots[1]
                                thirdPropNum = numIndividualEmptyHouseSlots[2]
                                props = [firstPropNum]

                                potentialProps = ["first", "second", "third"]


                                for d in propOrder:
                                    print("IDk")
                                    if d == thirdPropNum:
                                        print("third")
                                        if "third" in potentialProps:
                                            propNameOrder.append("third")
                                            potentialProps.pop(len(potentialProps)-1)
                                        elif d == secondPropNum:
                                            print("second inside")
                                            if "second" in potentialProps:
                                                print("second exists")
                                                propNameOrder.append("second")
                                                if "first" in potentialProps:
                                                    potentialProps.pop(len(potentialProps) - 1)
                                                elif "third" in potentialProps:
                                                    potentialProps.pop(0)
                                            elif d == firstPropNum:
                                                print("first inside")
                                                if "first" in potentialProps:
                                                    print("first exists")
                                                    propNameOrder.append("first")
                                                    potentialProps.pop(0)
                                    elif d == secondPropNum:
                                        print("second")
                                        if "second" in potentialProps:
                                            propNameOrder.append("second")
                                            if "first" in potentialProps:
                                                potentialProps.pop(len(potentialProps)-1)
                                            elif "third" in potentialProps:
                                                potentialProps.pop(0)
                                        elif d == firstPropNum:
                                            if "first" in potentialProps:
                                                propNameOrder.append("first")
                                                potentialProps.pop(0)
                                            elif d == thirdPropNum:
                                                if "third" in potentialProps:
                                                    propNameOrder.append("third")
                                                    potentialProps.pop(len(potentialProps) - 1)
                                    elif d == firstPropNum:
                                        print("first")
                                        if "first" in potentialProps:
                                            propNameOrder.append("first")
                                            potentialProps.pop(0)
                                        elif d == secondPropNum:
                                            if "second" in potentialProps:
                                                propNameOrder.append("second")
                                                if "first" in potentialProps:
                                                    potentialProps.pop(len(potentialProps) - 1)
                                                elif "third" in potentialProps:
                                                    potentialProps.pop(0)
                                            elif d == thirdPropNum:
                                                if "third" in potentialProps:
                                                    propNameOrder.append("third")
                                                    potentialProps.pop(len(potentialProps) - 1)

                            # Get the property names in order
                            if len(propNameOrder) != 0:
                                propNameListOrder = []
                                propNames = self.real_estate_manager.get_prop_Names(colours[i])
                                print("Getting prop names = ", propNames)
                                print("Prop name order = ", propNameOrder)
                                print("Prop num order = ", )
                                for j in propNameOrder:
                                    if j == "first":
                                        propNameListOrder.append(propNames[0])
                                    elif j == "third":
                                        propNameListOrder.append(propNames[len(propNames)-1])
                                    elif j == "second":
                                        if "first" in propNameOrder:
                                            propNameListOrder.append(propNames[1])
                                        elif "third" in propNameOrder:
                                            propNameListOrder.append(propNames[0])
                                        else:
                                            propNameListOrder.append(0)

                                # Build
                                while potentialHouses > 0:
                                    print("Potential Hotels = ", potentialHotels)
                                    print("PropNameListOrder = ", propNameListOrder)
                                    print("Houses left = ", self.real_estate_manager.available_houses)
                                    print("Hotels left = ", self.real_estate_manager.available_hotels)
                                    print("potentialHOuses = ", potentialHouses)
                                    for k in range(len(propNameListOrder)):
                                        if potentialHouses > 0:
                                            if propOrder[k] > 1:
                                                self.real_estate_manager.build_real_estate(1, propNameListOrder[k], player_name, self.property_manager)
                                                self.real_estate_manager.available_houses -= 1
                                                potentialHouses -= 1
                                            elif propOrder[k] == 1:
                                                self.real_estate_manager.build_real_estate(1, propNameListOrder[k], player_name, self.property_manager)
                                                self.real_estate_manager.available_hotels -= 1
                                                potentialHotels -=1
                                            else:
                                                pass



            if player_name[0] != "N":
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
            player_counter += 1
            turnNum += 1
            if player_counter == len(self.players):
                player_counter = 0
            else:
                pass
            # Debugged




if __name__ == "__main__":
    main = Main()
    main.main()
