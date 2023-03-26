def truncate(n):
    multiplier = 10
    return int(n * multiplier)/multiplier

def getTotals(categories):
    total = 0
    breakdown = []
    for category in categories:
        total += category.get_withdrawals()
    rounded = list(map(lambda x: truncate(x/total), breakdown))
    return rounded


def create_spend_chart(categories):
    result = "Percentage spent by category\n"
    i = 100
    totals = getTotals(categories)

    while i >= 0:
        spaces = " "
        for total in totals:
            if total * 100 >= i:
                spaces += "o  "
            else:
                spaces += "  "
        result += str(i).rjust(3) + "|" + spaces + ("\n")
        i -= 10
    
    dashes = "-" + "---" * len(categories)
    names = []
    xAxis = ""
    for category in categories:
        names.append(category.name)
    max_i = max(names, key=len)

    for n in range(len(max_i)):
        nameStr = '     '
        for name in names:
            if n >= len(name):
                nameStr += "   "
            else:
                nameStr += name[n] + " "

        if n != (len(max_i) - 1):
            nameStr += '\n'

        xAxis += nameStr

    result += dashes.rjust(len(dashes)+4) + '\n' + xAxis
    return result

class Category:

    def __init__(self, name):
        self.name = name
        self.ledger = list()

    def __str__(self):
        header = f"{self.name: *^30}"
        items = ''
        total = 0
        for i in self.ledger:
            items += f"{i['description'][0:23]:23}" + f"{i['amount']:>7.2f}" + '\n'
            total += i['amount']
        output = header + items + "Total: " + str(total)
        return output
    
    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
        
    def withdraw(self, amount, description=''):
        if (self.check_funds(amount)):
            self.ledger.append({'amount': -1 * amount, 'description': description})
            return True
        else:
            return False
        
    def get_balance(self):
        account_balance = 0
        for i in self.ledger:
            account_balance += i['amount'] 
        return account_balance
    
    def transfer(self, amount, category):
        if(self.check_funds(amount)):
            self.withdraw(amount, 'Tranfer to ' + category.name)
            category.deposit(amount, 'Transfer from ' + self.name)
            return True
        else:
            return False
        
    def check_funds(self, amount):
        if(self.get_balance() >= amount):
            return True
        else:
            return False
        
    def get_withdrawls(self):
        total = 0
        for i in self.ledger:
            if i['amount'] < 0:
                total += i['amount']
        return total
