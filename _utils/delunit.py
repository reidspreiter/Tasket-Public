# Stores and formats information of a single delinquent unit
class DelUnit:

    def __init__(self, primary, unit_number, balance):
        self.primary = self.format_name(primary)
        self.initials = self.format_initials()
        self.occupants = self.primary
        self.guarantor = "N/A"
        self.unit_number = unit_number
        self.address = self.format_address()
        self.balance = self.format_balance(balance)
        self.balance_in_words = self.format_balance_in_words(self.balance)


    def add_guarantor(self, guarantor):
        guarantor = self.format_name(guarantor)
        if self.guarantor == "N/A":
            self.guarantor = guarantor
        else:
            self.guarantor += f" and {guarantor}"


    def add_occupant(self, occupant):
        occupant = self.format_name(occupant)
        self.occupants += f" and {occupant}"


    def format_name(self, name):
        #remove any parenthetical nicknames
        if name.find("(") != -1:                                                
            name = (name[ : name.index("(") : ] 
                    + name[name.index(")") + 1 : : ])

        name = name.split(", ")
        first = name[1]                                
        last = name[0]                                             

        if first[-1] != " ":                                                    
            first += " "
        return first + last                                                     


    def format_initials(self):
        name = self.primary.split()
        return name[0][0] + name[1][0]


    def format_address(self):
        if self.unit_number < 101:
            return f"Address {self.unit_number}"
        return f"Address {self.unit_number}"


    def format_balance(self, balance):
        return balance[:(balance.index('.') + 3)] 


    def format_balance_in_words(self, balance):
        ones_digits = ["", "One ", "Two ", "Three ", "Four ", "Five ", 
                       "Six ", "Seven ", "Eight ", "Nine "]
        tens_digits = ["", "", "Twenty ", "Thirty ", "Forty ", "Fifty ", 
                       "Sixty ", "Seventy ", "Eighty ", "Ninety "]
        teen_digits = ["Ten", "Eleven ", "Twelve ", "Thirteen ", 
                       "Fourteen ", "Fifteen ", "Sixteen ", 
                       "Seventeen ", "Eighteen ", "Nineteen "]
        balance_in_words = ""

        if len(balance) == 8:
            balance_in_words += ones_digits[int(balance[0])] + "Thousand "
            balance = balance[2:]

        if len(balance) == 6:
            if balance[0] != '0':
                balance_in_words += ones_digits[int(balance[0])] + "Hundred "
            balance = balance[1:]

        if balance_in_words != "":
            balance_in_words += "& "

        if len(balance) == 5:
            if balance[0] == '1':
                balance_in_words += teen_digits[int(balance[1])]
                balance = balance[3:]
            else:
                balance_in_words += tens_digits[int(balance[0])]
                balance = balance[1:]

        if len(balance) == 4:
            balance_in_words += ones_digits[int(balance[0])]
            balance = balance[2:]
        
        # balance_in_words now stores dollar amount, and balance stores cent amount
        return balance_in_words + "Dollars     " + balance + "/100"