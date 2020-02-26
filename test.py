import database_creator

class database():

    def __init__(self):
        self.db = database_creator.get_database()

    def read_value(self, row, column):
        """Gets specifed information about thing of interest
        Inputs: Row is string that is the name of what we want to know about. Column is a string name of type of info
        we want to get
        Output: A string with the speicified information
        Class_vars_modified: none
        """

        # you still watching? y. Ok here's a little thing i never showed you, but it will simplify below.
        # means you don't need an entire block of ORs. Ok? Just nicer code, and will be better to read. Ok, I will change it. Thanks so much. alright i'm going to log off. ok
        if column in ["name", "owner", "is_available_for_purchase", "price", "real_estate_price", "rent",
                      "num_of_houses", "is_mortgaged", "price_for_one_house", "price_for_two_houses",
                      "price_for_three_houses", "price_for_four_houses", "price_for_one_hotel", "property_type",
                      "rent_for_one_railroad", "rent_for_two_railroads", "rent_for_three_railroads",
                      "rent_for_four_railroads", "board_position"]:
            print(True)
            final = self.db.query("SELECT " + column + " FROM main_property_deck WHERE name = :row", row=row)
        elif column in ["player_name", "spot_on_board", "money", "num_get_out_of_jail", "is_in_jail", "num_of_doubles"]:
            final = self.db.query("SELECT " + column + " FROM player_information WHERE player_name = :row", row=row)
        elif column in ["chance_name"]:
            final = self.db.query("SELECT " + column + " FROM chance_cards WHERE chance_name = :row", row=row)
        elif column in ["community_chest_name"]:
            final = self.db.query("SELECT " + column + " FROM community_chest_cards WHERE community_chest_name = :row", row=row)
        else:
            # if the column doesn't exist anywhere (ie. a typo) return none
            return None

        result = final.first(as_dict=True)[column]
        self.db.close()
        return result


if __name__ == "__main__":
    a = database()
    print(a.read_value("Player 2", "money"))

