import database
import database_creator
import movement_manager

class PropertyManager:

    #public
    def __init__(self):
        self.db = database.Database()
        self.row = []
        self.roww = []
        self.row_final = []
        self.a = database.Database()
        self.movement_manager = movement_manager.MovementManager()

    def get_is_property_available(self, property_name):
        """Returns a specified property's purchase status
        Inputs: property_name(str)
        Outputs: yes or no(str)"""

        property_availability = self.db.read_value(property_name, "is_available_for_purchase")
        return property_availability

    def get_property_price(self, property_name):
        """Returns the price of a specified property.
        Input: property_name (string) - the name of the property
        Output: (int) the price to buy the property
        """
        property_price = self.db.read_value(property_name, "price")
        return int(property_price)

    def get_property_real_estate_price(self, property_name):
        """Returns cost of building house/hotel on a specified property.
        Input: property_name (string) - the name of the property
        Output: (int) the price to build house/hotel
        """
        real_estate_price = self.db.read_value(property_name, "real_estate_price")
        return int(real_estate_price)

    def get_property_real_estate_payout(self, property_name, num_pieces):
        """Returns rent of property with specified num of real estate built.
        Input: property_name (string) - the name of the property. num_pieces (int) num pieces of real estate on property
        Output: (int) the cost of rent
        """
        if (num_pieces == 0):
            rent = self.db.read_value(property_name, "rent")
            return int(rent)
        elif (num_pieces == 1) :
            rent = self.db.read_value(property_name, "price_for_one_house")
            return int(rent)
        elif (num_pieces == 2) :
            rent = self.db.read_value(property_name, "price_for_two_houses")
            return int(rent)
        elif (num_pieces == 3) :
            rent = self.db.read_value(property_name, "price_for_three_houses")
            return int(rent)
        elif (num_pieces == 4) :
            rent = self.db.read_value(property_name, "price_for_four_houses")
            return int(rent)
        elif (num_pieces == 5) :
            rent = self.db.read_value(property_name, "price_for_one_hotel")
            return int(rent)

    def get_owner(self, property_name):
        """Returns the owner of a specified property as a string
        Inputs: property_name(str)
        Outputs: name of the owner(str)"""

        property_owner = self.db.read_value(property_name, "owner")
        return property_owner

    def get_num_houses(self, property_name):
        """Returns the number of houses on a specific property as an integer
        Inputs: property_name(str)
        Outputs: num_houses(int)"""

        num_houses = self.db.read_value(property_name, "num_of_houses")
        return int(num_houses)

    def get_monopolies(self):
        """Returns the owner and colour of all monopolies on the board
        Inputs: None
        Outputs: Owner and colour in a list of lists"""

        purple = self.get_colour_monopolies_owner("purple")
        grey = self.get_colour_monopolies_owner("grey")
        pink = self.get_colour_monopolies_owner("pink")
        orange = self.get_colour_monopolies_owner("orange")
        red = self.get_colour_monopolies_owner("red")
        yellow = self.get_colour_monopolies_owner("yellow")
        green = self.get_colour_monopolies_owner("green")
        blue = self.get_colour_monopolies_owner("blue")
        railroad = self.get_other_monopolies_owner("railroad")
        utility = self.get_other_monopolies_owner("utility")

        if (purple[0][0] == purple[1][0]) and (purple[0][0] and purple[1][0] != ""):
            self.row_final.append(purple[0])
            self.a.write_value("is_a_monopoly", "yes", "Baltic Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Mediterranean Ave.")

        if (grey[0][0] == grey[1][0] == grey[2][0]) and (grey[0][0] and grey[1][0] and grey[2][0] != ""):
            self.row_final.append(grey[0])
            self.a.write_value("is_a_monopoly", "yes", "Oriental Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Vermont Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Connecticut Ave.")

        if (pink[0][0] == pink[1][0] == pink[2][0]) and (pink[0][0] and pink[1][0] and pink[2][0] != ""):
            self.row_final.append(pink[0])
            self.a.write_value("is_a_monopoly", "yes", "St. Charles Place")
            self.a.write_value("is_a_monopoly", "yes", "States Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Virginia Ave.")

        if (orange[0][0] == orange[1][0] == orange[2][0]) and (orange[0][0] and orange[1][0] and orange[2][0] != ""):
            self.row_final.append(orange[0])
            self.a.write_value("is_a_monopoly", "yes", "St. James Place")
            self.a.write_value("is_a_monopoly", "yes", "Tennessee Ave.")
            self.a.write_value("is_a_monopoly", "yes", "New York Ave.")

        if (red[0][0] == red[1][0] == red[2][0]) and (red[0][0] and red[1][0] and red[2][0] != ""):
            self.row_final.append(red[0])
            self.a.write_value("is_a_monopoly", "yes", "Kentucky Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Indiana Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Illinois Ave.")

        if (yellow[0][0] == yellow[1][0] == yellow[2][0]) and (yellow[0][0] and yellow[1][0] and yellow[2][0] != ""):
            self.row_final.append(yellow[0])
            self.a.write_value("is_a_monopoly", "yes", "Atlantic Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Ventnor Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Marvin Gardens")

        if (green[0][0] == green[1][0] == green[2][0]) and (green[0][0] and green[1][0] and green[2][0] != ""):
            self.row_final.append(green[0])
            self.a.write_value("is_a_monopoly", "yes", "Pacific Ave.")
            self.a.write_value("is_a_monopoly", "yes", "North Carolina Ave.")
            self.a.write_value("is_a_monopoly", "yes", "Pennsylvania Ave.")

        if (blue[0][0] == blue[1][0]) and (blue[0][0] and blue[1][0] != ""):
            self.row_final.append(blue[0])
            self.a.write_value("is_a_monopoly", "yes", "Park Place")
            self.a.write_value("is_a_monopoly", "yes", "Boardwalk")


        if (railroad[0][0] == railroad[1][0] == railroad[2][0] == railroad[3][0]) and (railroad[0][0] and railroad[1][0] and railroad[2][0] and railroad[3][0] != ""):
            self.row_final.append(railroad[0])
            self.a.write_value("is_a_monopoly", "yes", "Reading Railroad")
            self.a.write_value("is_a_monopoly", "yes", "Pennsylvania Railroad")
            self.a.write_value("is_a_monopoly", "yes", "B. & O. Railroad")
            self.a.write_value("is_a_monopoly", "yes", "Short Line")

        if (utility[0][0] == utility[1][0]) and (utility[0][0] and utility[1][0] != ""):
            self.row_final.append(utility[0])
            self.a.write_value("is_a_monopoly", "yes", "Electric Company")
            self.a.write_value("is_a_monopoly", "yes", "Water Works")

        else:
            None

        print(self.row_final)
        return self.row_final


    def update_houses(self, num_of_houses, prop_name):#not done
        """Change the amount of houses a property has in the database
            Inputs: number of houses that are going to be bought or sold(int), the property they are being build on or sold from(str)
            Outputs: None"""
        self.db.write_value("num_of_houses", str(num_of_houses), prop_name)
        return True


    def buy_property(self, player_name):
        """
        Buys a property. Gets all the values within the function. Only param is player_name
        :param player_name: Name of the player
        :return: None
        """
        current_property_name = self.get_current_property_name(player_name)
        balance_before_purchase = self.get_balance(player_name)
        property_cost = self.get_property_price(current_property_name)
        new_balance = balance_before_purchase - property_cost

        if self.get_is_property_available(current_property_name) == "yes":
            if balance_before_purchase >= property_cost:
                self.db.write_value("is_available_for_purchase", "no", current_property_name)
                self.db.write_value("owner", player_name, current_property_name)
                self.db.write_value("money", new_balance, player_name)
            else:
                print("You do not have enough money to buy this property")
        else:
            print("This property is not available for purchase")







    #private

    def get_colour_monopolies_owner(self, prop_colour):
        """Is a query template that takes in prop_colour and returns if the colour has a monopoly. Is only used in get_monopolies()
            Inputs: prop_colour(str)
            Outputs: if the specific colour has a monopoly (yes or no(str))"""

        colour_monopolies = database_creator.db.query(
            "SELECT owner FROM main_property_deck WHERE property_colour = :prop_colour", prop_colour=prop_colour)
        self.row = []
        for i in colour_monopolies:
            d = i.owner, prop_colour
            self.row.append(d)
        #print(self.row)
        return self.row

    def get_other_monopolies_owner(self, prop_colour):
        """Is a query template that takes in prop_colour and returns if the colour has a monopoly. Is only used in get_monopolies()
            Inputs: prop_colour(str), prop_colour holds prop_type. It is the same variable so that below I can see if a colour property or a utility/railroad is inputed
            Outputs: if the specific colour has a monopoly (yes or no(str))"""

        other_monopolies = database_creator.db.query(
            "SELECT owner FROM main_property_deck WHERE property_type = :prop_colour",
            prop_colour=prop_colour)  # prop_colour is holding prop type
        self.roww = []
        for j in other_monopolies:
            h = j.owner, prop_colour
            self.roww.append(h)
        #print(self.roww)
        return self.roww

    def get_row_final(self):
        print(self.row_final)
        return self.row_final






    def get_current_property_name(self, player_name):
        """
        Gets the name of the property a player is currently on
        :param player_name: name of the player
        :return: The name of the property a player is currently on (str)
        """
        current_location_num = self.movement_manager.get_current_location_value(player_name)
        current_property_name = self.db.specific_read_value(current_location_num, "board_position", "name")
        return current_property_name

    def get_current_property_owner(self, player_name):
        """
        Gets the owner of the property a player is currently on
        :param player_name: Name of the player (str)
        :return: The owner of a property the player is currently on (str)
        """
        current_location_num = self.movement_manager.get_current_location_value(player_name)
        current_prop_owner = self.db.specific_read_value(current_location_num, "board_position", "owner")
        return current_prop_owner


    def get_balance(self, player_name):
        """
        Return's a player's total monety
        :param player_name: Name of the player you are getting the balance from (str)
        :return: The amount of money they have (int)
        """
        balance = int(self.db.read_value(player_name, "money"))
        return balance



if __name__ == "__main__":
    a = PropertyManager()
    #a.get_monopolies()
    print(a.buy_property("Player 2"))
    #b = database.Database()
    #a.get_row_final()
    #b.write_value("is_available_for_purchase", "no", "Baltic Ave.")


