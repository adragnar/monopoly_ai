import database
import random


class MovementManager:

    # Public
    def __init__(self):
        self.db = database.Database()
        self.roll = 0

    def roll_dice(self, player_name):
        """
        Rolls the dice
        :param player_name: rlly bruh
        :return: A list storing the roll and each dice val separately
        """
        roll = input("Enter each dice value for " + player_name + "'s roll side by side: ")
        self.roll = int(roll[0]) + int(roll[1])
        dice1 = int(roll[0])
        dice2 = int(roll[1])
        roll = dice1 + dice2
        return [roll, dice1, dice2]

    def roll_dice_in_jail(self, player_name):
        """
        Rolls dice in jail
        :param player_name: player name
        :return: None
        """
        roll = self.roll_dice(player_name)
        roll = roll[0]
        self.move(player_name, roll)

    def npcDiceRoll(self):
        """
        Performs a dice roll for NPC players
        :return: None
        """
        dice1 = random.randint(1,6)
        dice2 = random.randint(1,6)
        roll = dice1 + dice2
        return [roll, dice1, dice2]

    def getNumJailRolls(self, player_name):
        """
        Returns however many rolls the current player has had in jail
        :param player_name: Name of player
        :return: num rolls player has in jail (int)
        """
        numRolls = int(self.db.read_value(player_name, "jail_roll_counter"))
        return numRolls

    def incrementJailRolls(self, player_name):
        """
        Increments the number of rolls in jail
        :param player_name: player name
        :return: None
        """
        currentNumRolls = int(self.db.read_value(player_name, "jail_roll_counter"))
        newNumRolls = currentNumRolls + 1
        self.db.write_value("jail_roll_counter", str(newNumRolls), player_name)

    def resetJailRolls(self, player_name):
        """
        Reset the player's jail rolls to 0
        :param player_name: player name
        :return: None
        """
        self.db.write_value("jail_roll_counter", "0", player_name)

    def getNumDoubleRolls(self, player_name):
        """
        Get the number of double rolls the player currently has
        :param player_name: player name
        :return: Num of current double rolls (int)
        """
        numRolls = self.db.read_value(player_name, "double_roll_counter")
        return int(numRolls)

    def incrementDoubleRolls(self, player_name):
        """
        Increment the player's number of double rolls
        :param player_name: player name
        :return: None
        """
        currentNumRolls = int(self.getNumDoubleRolls(player_name))
        newNumRolls = currentNumRolls + 1
        self.db.write_value("double_roll_counter", str(newNumRolls), player_name)

    def resetNumDoubleRolls(self, player_name):
        """
        Reset the player's number of double rolls
        :param player_name: Player name
        :return: None
        """
        self.db.write_value("double_roll_counter", "0", player_name)

    def move(self, player_name, number_of_spaces):
        """
        Moves the player to their place after their roll
        :param player_name: Name of player (str)
        :param number_of_spaces: the player's roll or how many spaces they need to move.(int)
        :return: None
        """
        self.check_for_go_money(player_name, str(number_of_spaces))
        current_location_value = int(self.get_current_location_value(player_name))
        new_location_value = current_location_value + number_of_spaces

        if new_location_value >= 40:
            new_location_value = new_location_value - 40
        else:
            pass

        self.db.write_value("spot_on_board", str(new_location_value), player_name)

    def go_to_jail(self, player_name):
        """
        Puts a player in jail
        :param player_name: Name of player
        :return: None
        """
        print("YOU ARE IN JAIL!")
        self.db.write_value("is_in_jail", "yes", player_name)
        self.db.write_value("spot_on_board", "10", player_name)

    def advance_to_stcharles_place(self, player_name):
        """
        Puts a player in St.Charles Place
        :param player_name: Name of player
        :return: None
        """
        current_location_value = int(self.get_current_location_value(player_name))
        if current_location_value > 11:
            distance_traveled = (40 - current_location_value) + 11
        elif current_location_value == 11:
            distance_traveled = 0
        else:
            distance_traveled = 11 - current_location_value
        self.check_for_go_money(player_name, distance_traveled)
        self.db.write_value("spot_on_board", "11", player_name)

    def advance_to_boardwalk(self, player_name):
        """
        Puts a player in boardwalk
        :param player_name: Name of player
        :return: None
        """
        current_location_value = int(self.get_current_location_value(player_name))
        if current_location_value == 39:
            distance_traveled = 0
        else:
            distance_traveled = 39 - current_location_value
        self.check_for_go_money(player_name, distance_traveled)
        self.db.write_value("spot_on_board", "39", player_name)

    def advance_to_nearest_railroad(self, player_name):
        """
        Will put you in the nearest railroad
        :param player_name: Name of player
        :return: None
        """
        current_location_value = int(self.get_current_location_value(player_name))
        if 0 <= current_location_value <= 5 or 36 <= current_location_value <= 39:
            self.db.write_value("spot_on_board", "5", player_name)
            # Go money
            current_balance = int(self.db.read_value(player_name, "money"))
            new_balance = current_balance + 200
            self.db.write_value("money", str(new_balance), player_name)
        elif 6 <= current_location_value <= 15:
            self.db.write_value("spot_on_board", "15", player_name)
        elif 16 <= current_location_value <= 25:
            self.db.write_value("spot_on_board", "25", player_name)
        elif 26 <= current_location_value <= 35:
            self.db.write_value("spot_on_board", "35", player_name)
        else:
            print("pass")

    def advance_to_nearest_utility(self, player_name):
        """
        Put you in the nearest utility
        :param player_name: name of player
        :return: None
        """
        current_location_value = int(self.get_current_location_value(player_name))
        if 13 <= current_location_value <= 28:
            self.db.write_value("spot_on_board", "28", player_name)
        else:
            if 29 <= current_location_value <= 39:
                current_balance = int(self.db.read_value(player_name, "money"))
                new_balance = current_balance + 200
                self.db.write_value("money", str(new_balance), player_name)
            self.db.write_value("spot_on_board", "12", player_name)

    def go_back_3_spaces(self, player_name):
        """
        Brings a player back 3 spaces
        :param player_name: Name of player
        :return: None
        """
        current_location_value = int(self.get_current_location_value(player_name))
        new_current_location_value = current_location_value - 3
        self.db.write_value("spot_on_board", str(new_current_location_value), player_name)

    def check_get_out_cards(self, player_name):
        """
        Will check to see if you have a get out of jail free card
        :param player_name: Name of player
        :return: Bool indicating if u have it or not
        """
        if self.db.read_value(player_name, "num_get_out_of_jail") > 0:
            return True
        else:
            return False

    def leave_jail(self, player_name):
        """
        Will put the player out of jail
        :param player_name: Name of player
        :return: None
        """
        self.db.write_value("num_get_out_of_jail", "0", player_name)
        self.db.write_value("is_in_jail", "no", player_name)


    # Private
    def check_for_go_money(self, player_name, number_of_spaces):
        """
        Will check for go money and if the player passes go it will be added
        :param player_name: Name of player
        :param number_of_spaces: Number of spaces the player is travelling this turn
        :return: None
        """
        current_location_value = int(self.get_current_location_value(player_name))
        if current_location_value + int(number_of_spaces) >= 40:
            print("You have passed go!")
            current_balance = int(self.db.read_value(player_name, "money"))
            new_balance = str(current_balance + 200)
            self.db.write_value("money", new_balance, player_name)
        else:
            pass

    def get_current_location_value(self, player_name):
        """
        Gets a players numerical location on the board (str)
        :param player_name: Name of player (str)
        :return: a player's numerical location on the board (str)
        """
        current_location_value = self.db.read_value(player_name, "spot_on_board")
        return current_location_value

    def is_in_jail(self, player_name):
        """
        Will return True if the player is in jail and False if they are not
        :param player_name: Name of player
        :return: True if player is in jail and False if they are not
        """
        if self.db.read_value(player_name, "is_in_jail") == "yes":
            return True
        else:
            return False


if __name__ == "__main__":
    a = MovementManager()
    a.roll_dice("Player 1")
