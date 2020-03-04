import database_creator


class Database:

    def __init__(self):
        self.db = database_creator.get_database()

    def read_value(self, row, column):
        """Gets specifed information about thing of interest
        Inputs: Row is string that is the name of what we want to know about. Column is a string name of type of info
        we want to get
        Output: A string with the speicified information
        Class_vars_modified: none
        """
        # means you don't need an entire block of ORs. Ok? Just nicer code, and will be better to read.
        if column in ["name", "owner", "is_available_for_purchase", "price", "real_estate_price", "rent",
                      "num_of_houses", "is_mortgaged", "price_for_one_house", "price_for_two_houses",
                      "price_for_three_houses", "price_for_four_houses", "price_for_one_hotel", "property_type",
                      "rent_for_one_railroad", "rent_for_two_railroads", "rent_for_three_railroads",
                      "rent_for_four_railroads", "board_position", "property_colour", "is_a_monopoly"]:
            final = self.db.query("SELECT " + column + " FROM main_property_deck WHERE name = :row", row=row)
        elif column in ["player_name", "spot_on_board", "money", "num_get_out_of_jail", "is_in_jail", "num_of_doubles", "double_roll_counter"]:
            final = self.db.query("SELECT " + column + " FROM player_information WHERE player_name = :row", row=row)
        elif column in ["chance_name", "chance_money_gained", "chance_money_lost", "chance_move_forward",
                        "chance_move_backward"]:
            final = self.db.query("SELECT " + column + " FROM chance_cards WHERE chance_name = :row", row=row)
        elif column in ["community_chest_name", "community_chest_money_gained", "community_chest_money_lost",
                        "community_chest_move_forward", "community_chest_move_backward"]:
            final = self.db.query("SELECT " + column + " FROM community_chest_cards WHERE community_chest_name = :row", row=row)
        else:
            # if the column doesn't exist anywhere (ie. a typo) return none
            return None

        result = final.first(as_dict=True)[column]
        print(result)
        return result


    def specific_read_value(self, row, search_column, column):
        """
        It is used in Rent_Manager() class. It allows you to specify each aspect of the search. Only needed in certain scenarios
        :param row: Row is string that is the name of what we want to know about.
        :param search_column: This is the column that we are trying to find row in
        :param column: Column is a string name of type of info we want to get
        :return: A string with the speicified information
        """
        if column in ["name", "owner", "is_available_for_purchase", "price", "real_estate_price", "rent",
                      "num_of_houses", "is_mortgaged", "price_for_one_house", "price_for_two_houses",
                      "price_for_three_houses", "price_for_four_houses", "price_for_one_hotel", "property_type",
                      "rent_for_one_railroad", "rent_for_two_railroads", "rent_for_three_railroads",
                      "rent_for_four_railroads", "board_position", "property_colour", "is_a_monopoly"]:
            final = self.db.query("SELECT " + column + " FROM main_property_deck WHERE " + search_column + " = :row", row=row)
        elif column in ["player_name", "spot_on_board", "money", "num_get_out_of_jail", "is_in_jail", "num_of_doubles"]:
            final = self.db.query("SELECT " + column + " FROM player_information WHERE " + search_column + " = :row", row=row)
        elif column in ["chance_name", "chance_money_gained", "chance_money_lost", "chance_move_forward",
                        "chance_move_backward"]:
            final = self.db.query("SELECT " + column + " FROM chance_cards WHERE " + search_column + " = :row", row=row)
        elif column in ["community_chest_name", "community_chest_money_gained", "community_chest_money_lost",
                        "community_chest_move_forward", "community_chest_move_backward"]:
            final = self.db.query("SELECT " + column + " FROM community_chest_cards WHERE " + search_column + " = :row", row=row)
        else:
            # if the column doesn't exist anywhere (ie. a typo) return none
            return None

        result = final.first(as_dict=True)[column]
        print(result)
        return result


    def write_value(self, column, value, row):
        """replaces/updates specific information in the database
                Inputs: Row is string that is the new value. Column is a string name of type of info
                we want to replace
                Output: none
                Class_vars_modified: none
                """
        if column in ["name", "owner", "is_available_for_purchase", "price", "real_estate_price", "rent",
                      "num_of_houses", "is_mortgaged", "price_for_one_house", "price_for_two_houses",
                      "price_for_three_houses", "price_for_four_houses", "price_for_one_hotel", "property_type",
                      "rent_for_one_railroad", "rent_for_two_railroads", "rent_for_three_railroads",
                      "rent_for_four_railroads", "board_position", "property_colour", "is_a_monopoly"]:
            self.db.query("UPDATE main_property_deck SET " + column + " = :value WHERE name = :row", row=row, value=value)
        elif column in ["player_name", "spot_on_board", "money", "num_get_out_of_jail", "is_in_jail", "num_of_doubles"]:
            self.db.query("UPDATE player_information SET " + column + " = :value WHERE player_name =  + :row", row=row, value=value)
        elif column in ["chance_name", "chance_money_gained", "chance_money_lost", "chance_move_forward",
                        "chance_move_backward"]:
            self.db.query("UPDATE chance_cards SET " + column + " = :value + WHERE chance_name = :row", row=row, value=value)
        elif column in ["community_chest_name", "community_chest_money_gained", "community_chest_money_lost",
                        "community_chest_move_forward", "community_chest_move_backward"]:
            self.db.query("UPDATE community_chest_cards SET " + column + " = :value WHERE community_chest_name = :row", row=row, value=value)
        else:
            # if the column doesn't exist anywhere (ie. a typo) return none
            return "That column does not exist"

if __name__ == "__main__":
    a = Database()
    print(a.specific_read_value("60", "price_for_one_house", "name"))


