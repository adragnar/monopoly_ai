class real_estate_manager() :

    #public
    def __init__(self):
        available_houses = 32
        available_hotels = 12

    def build_real_estate(self):

    def sell_real_estate(self):


    #private
    def can_build(self, is_house):
        """Determines whether it is possible to build a house or hotel. 
         Input: is_house, bool that is 1 if want to build house, 0 if want to build hotel
         Return: bool indicating whether can build 
         Class_vars_mod_: none
         """
        if is_house:
            if self.available_houses == 0:
                return False
            else:
                return True

        else:
            if self.available_hotels == 0:
                return False
            else:
                return True
