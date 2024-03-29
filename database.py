import numpy as np
import pandas as pd
from datetime import date, timedelta
import datetime
import calendar


#Where we store a person's income dictionary and spending dictionary
#Each Dictionary consists of a dictionary of lists, with keys as dates
#Able to append and access values for spending/income based on date
#Also manages limits on spending based on income
class Person:
    def __init__(self,name, income, spend = 0, monthlyIncome = 0.0 ):
        self.name = name
        self.income = {} 
        self.spend = {}
        self.needlimit = 0.5*monthlyIncome
        self.wantlimit = 0.3*monthlyIncome
        self.monthly_income = monthlyIncome

    
#Income and Spending functions
#2022-12-27  ----- example of date from date.today

# This will take in the current month and year and return the monthly income for it
    def get_total_monthly_income(self, month = datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        if month is None:
            month = datetime.datetime.now().month

        if year is None:
            year = datetime.datetime.now().year

        monthly = 0
        for i in range(1, 32):
            try:
                temp = datetime.date(year, month, i)
                if (temp in self.income):
                    income_list = self.income[temp]
                    for j in range(0, len(income_list)):
                        monthly += income_list[j].amount
            except ValueError:
                break
        return monthly
    
# This will take in the current month and year and return the monthly spend for it    
    def get_total_monthly_spending(self, month=None, year=None):
        if month is None:
            month = datetime.datetime.now().month

        if year is None:
            year = datetime.datetime.now().year

        monthly = 0
        for i in range(1, 32):
            try:
                temp = datetime.date(year, month, i)
                if (temp in self.spend):
                    spend_list = self.spend[temp]
                    for j in range(0, len(spend_list)):
                        monthly += spend_list[j].amount
            except ValueError:
                break
        return monthly


# This will take in the current month and year and return a dataframe for the monthly trend
    
    def get_trend_monthly_income(self, month = datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        monthly = 0 
        num_days = calendar.monthrange(year, month)[1]
        
        #days = [datetime.date(year, month, day) for day in range (1, num_days+1)]
        income_days = []
        days = []

        for i in range (1, num_days+1):
            temp = datetime.date(year, month, i)
            if (temp in self.income):
                income_list = self.income[temp]
                for j in range(0, len(income_list)):
                    monthly += income_list[j].amount
                income_days.append(monthly)
                days.append(i)
        trend = pd.DataFrame({'Days': days, 'Income': income_days})
        return(trend)

# Returns data frame containing monthly spending, meant to have output be used in graphing spending trend
    def get_trend_monthly_spend(self, month = datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        monthly = 0 
        num_days = calendar.monthrange(year, month)[1]
        
        #days = [datetime.date(year, month, day) for day in range (1, num_days+1)]
        spend_days = []
        days = []

        for i in range (1, num_days+1):
            temp = datetime.date(year, month, i)
            if (temp in self.spend):
                spend_list = self.spend[temp]
                for j in range(0, len(spend_list)):
                    monthly += spend_list[j].amount
                spend_days.append(monthly)
                days.append(i)
        trend = pd.DataFrame({'Days': days, 'Spending': spend_days})
        return(trend)
    
    def get_trend_yearly_income(self, year = datetime.datetime.now().year):
        income_monthly = []
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_with_income = []

        for i in range(12):
            
            monthly_income = self.get_total_monthly_income(i + 1, year)
            if (monthly_income != 0):
                income_monthly.append(monthly_income)
                month_with_income.append(month[i])
                
        
        trend = pd.DataFrame({'Month': month_with_income, 'Income': income_monthly})
        return(trend)
    
    def get_trend_yearly_spend(self, year = datetime.datetime.now().year):
        spend_monthly = []
        month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        month_with_spend = []

        for i in range(12):
            
            monthly_spend = self.get_total_monthly_income(i + 1, year)
            if (monthly_spend != 0):
                spend_monthly.append(monthly_spend)
                month_with_spend.append(month[i])
                
        
        trend = pd.DataFrame({'Month': month_with_spend, 'Income': spend_monthly})
        return(trend)
     

# Returns a dataframe containing difference between spending and income in a month, used in monthly trend
    def get_trend_monthly_difference(self, month = datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        monthly = 0 
        num_days = calendar.monthrange(year, month)[1]
        
        #days = [datetime.date(year, month, day) for day in range (1, num_days+1)]
        dif_days = []
        days = []
        income_check = False
        spend_check = False
        for i in range (1, num_days+1):
            temp = datetime.date(year, month, i)
            if (temp in self.spend):
                spend_list = self.spend[temp]
                for j in range(0, len(spend_list)):
                    monthly -= spend_list[j].amount
                income_check = True
            if (temp in self.income):
                income_list = self.income[temp]
                for j in range(0, len(income_list)):
                    monthly += income_list[j].amount
                spend_check = True
            if (spend_check or income_check):
                dif_days.append(monthly)
                days.append(i)
            income_check = False
            spend_check = False
        trend = pd.DataFrame({'Days': days, 'Difference': dif_days})
        return(trend)
  

#Remove Transaction from Income from certain day if it exists
    def delete_income(self, transaction, dates = date.today()):
        if (dates in self.income) and (transaction in self.income[dates]):
            self.income[dates].remove(transaction)
        
#Remove Transaction from Spend from certain day if it exists
    def delete_spending(self, transaction, dates = date.today()):
        if (dates in self.spend) and (transaction in self.spend[dates]):
            self.spend[dates].remove(transaction)        

# Returns Spending/Income for one Day in a particular category
    
    def get_categorical_day_income(self, category, date):
        total = 0
        if date in self.income:
            for i in range(len(self.income[date])):
                if (self.income[date][i].category == category):
                    total += self.income[date][i].amount
        return total
        
    def get_categorical_day_spend(self, category, date):
        total = 0
        if date in self.spend:
            for i in range(len(self.spend[date])):
                if (self.spend[date][i].category == category):
                    total += self.spend[date][i].amount
        return total
    
# Returns the monthly Income/Spend for the specified category in the specified month    
    def get_categorical_monthly_income(self, category, month = datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        total = 0
        for date in self.income:
            if date.year == year and date.month == month:
                for i in range(len(self.income[date])):
                    if (self.income[date][i].category == category):
                        total += self.income[date][i].amount
        return total
    
    def get_categorical_monthly_spending(self, category, month = datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        total = 0
        for date in self.spend:
            if date.year == year and date.month == month:
                for i in range(len(self.spend[date])):
                    if (self.spend[date][i].category == category):
                        total += self.spend[date][i].amount
        return total
    
# Returns the yearly Income/Spend for the specified category in the specified year

    def get_categorical_yearly_income(self, category, year = datetime.datetime.now().year):
        total = 0
        for date in self.income:
            if date.year == year:
                for i in range(len(self.income[date])):
                    if (self.income[date][i].category == category):
                        total += self.income[date][i].amount
        
        return total
    
    def get_categorical_yearly_spend(self, category, year = datetime.datetime.now().year):
        total = 0
        for date in self.spend:
            if date.year == year:
                for i in range(len(self.spend[date])):
                    if (self.spend[date][i].category == category):
                        total += self.spend[date][i].amount
        
        return total

# Returns Income/Spending for all time for a particular category
    
    def get_total_categorical_income(self, category):
        total = 0
        for date in self.income:
            for i in range(len(self.income[date])):
                if (self.income[date][i].category == category):
                    total += self.income[date][i].amount
        return total
    
    def get_total_categorical_spend(self, category):
        total = 0
        for date in self.spend:
            for i in range(len(self.spend[date])):
                if (self.spend[date][i].category == category):
                    total += self.spend[date][i].amount
        return total

# Return Income/Spending for a certain category across an inputted interval of time    
    
    def get_categorical_x_spending(self, category, time_length, date = datetime.datetime.now()):
        total = 0
        today = date
        for i in range (1, time_length):
            if (today in self.spend) :
                spend_list = self.spend[today]
                for j in range(0, len(spend_list)):
                    if (spend_list[j].category == category):
                        total += spend_list[j].amount
            today = today + datetime.timedelta(days = 1)
        return(total)

    def get_categorical_x_income(self, category, time_length, date = datetime.datetime.now()):
        total = 0
        today = date
        for i in range (1, time_length):
            if (today in self.income) :
                income_list = self.income[today]
                for j in range(0, len(income_list)):
                    if (income_list[j].category == category):
                        total += income_list[j].amount
            today = today + datetime.timedelta(days = 1)
        return(total)
    
# Returns a dictionary containing all the Income/Spend for all the category in the class for the specified year

    def get_yearly_income_by_category(self, year):
        yearly_income = {}
        for date in self.income:
            if date.year == year:
                for item in self.income[date]:
                    if item.category in yearly_income:
                        yearly_income[item.category] += item.amount
                    else:
                        yearly_income[item.category] = item.amount
        return yearly_income
    
    def get_yearly_spend_by_category(self, year):
        yearly_spend = {}
        for date in self.spend:
            if date.year == year:
                for item in self.spend[date]:
                    if item.category in yearly_spend:
                        yearly_spend[item.category] += item.amount
                    else:
                        yearly_spend[item.category] = item.amount
        return yearly_spend
    
    
    
    def get_x_spending(self,  time_length, day, month= datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        total = []
        count = day
        month_track = month
        for i in range (1, time_length):

            temp = str(year) + "-" + str(month_track) + "-" + str(count)
            if (temp in self.spend) :
                spend_list = self.spend[temp]
                for j in range(0, len(spend_list)):
                    # if (spend_list[j].category == category):
                    total.append(spend_list[j]) 
        return(total)       
            
        
    # def get_x_income(self,  time_length, day, month= datetime.datetime.now().strftime("%B"), year = datetime.datetime.now().year):
        


# This takes in an object of class income and appned it to the list of values in the dictionary with todays date as the key               
    def add_income(self, transaction, dates = date.today()):
        if dates in self.income:
            self.income[dates].append(transaction)
        else:
            self.income[dates] = [transaction]

# # This takes in an object of class spend and appned it to the list of values in the dictionary with todays date as the key      
    def add_spending(self, transaction, dates = date.today()):
        if dates in self.spend:
            self.spend[dates].append(transaction)
        else:
            self.spend[dates] = [transaction]
        
        percentage = self.warning_spending(dates)
        if percentage > 0:
            print("You are going over the spending limit by ", percentage)

# This will return the total life income of the person    
    def get_total_income(self):
        total_income = 0.0
        for i in self.income:
            income_list = self.income[i]
            for j in range(0, len(income_list)):
                total_income += income_list[j].amount
        return(total_income)

# This will return the total income for today
    def get_day_total_income(self, dates = date.today()):
        if (self.income.get(dates) is None):
            return 0
        income_list = self.income[dates]
        total_income = 0.0
        for i in range(0, len(income_list)):
            total_income += income_list[i].amount
        return(total_income)

# This will return the total life spending of the person    
    def get_total_spending(self):
        total_spend = 0.0
        for i in self.spend:
            spend_list = self.spend[i]
            for j in range(0, len(spend_list)):
                total_spend += spend_list[j].amount
        return(total_spend)

# This will return the total spend of today for the person
    def get_day_total_spending(self, dates = date.today()):
        if (self.spend.get(dates) is None):
            return 0
        spend_list = self.spend[dates]
        total_spend = 0.0
        for i in range(0, len(spend_list)):
            total_spend -= spend_list[i].amount
        return(total_spend)

# This will return the difference in the life income and spend of the person
    def get_total_difference(self):
        total = 0
        total += self.get_total_income()
        total -= self.get_total_spending()
        return(total)

# This will return the difference in todays income and spend of the person        
    def get_day_total_difference(self, dates = date.today()):
        total = 0,0
        total += self.get_day_total_income()
        total -= self.get_day_total_income()
        return(total)  
    
    def warning_spending(self, dates = date.today()):
        monthlyincome = self.get_total_monthly_income(dates.month, dates.year)
        monthlyspend = self.get_total_monthly_spending(dates.month, dates.year)
        if (monthlyincome == 0):
            return 100
        check = monthlyspend/monthlyincome
        if (check < 0.8):
            return 0
        else:
            return (check-0.8)*100

    
#Income Class
#transaction_name is the name of the transaction
#amount is the amount of the transaction
#category is what the income is from (job, relative, gift)
#notes is any side notes the user would like to add
#type is the type of money it is (Cash, Credit, Debit)
class Income():
    def __init__(self, transaction_name, amount, category, notes, types):
        self.transaction_name = transaction_name
        self.amount = amount
        self.category = category
        self.notes = notes
        self.type = types

    def assign_name(self, _name):
        self.name = _name

#Spend Class
#transaction_name is the name of the transaction
#amount is the amount of the transaction
#category is what the spending is from (job, relative, gift)
#notes is any side notes the user would like to add
#type is the type of money it is (Cash, Credit, Debit)     
class Spend():
    def __init__(self, transaction_name, amount, category, notes, types):
        self.transaction_name = transaction_name
        self.amount = amount
        self.category = category
        self.notes = notes
        self.type = types


#Spending/Income Transaction Objects
spend = Spend("Groceries", 200, "Groceries", "", "Debit")
spend2 = Spend("Rent", 600, "Rent", "", "Debit")
spend3 = Spend("Party", 200, "Party", "", "Debit")
spend4 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend5 = Spend("Rent", 600, "Rent", "", "Debit")
spend6 = Spend("Party", 200, "Party", "", "Debit")
spend7 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend8 = Spend("Rent", 600, "Rent", "", "Debit")
spend9 = Spend("Party", 200, "Party", "", "Debit")
spend10 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend11 = Spend("Rent", 600, "Rent", "", "Debit")
spend12 = Spend("Party", 200, "Party", "", "Debit")
spend13 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend14 = Spend("Rent", 600, "Rent", "", "Debit")
spend15 = Spend("Party", 200, "Party", "", "Debit")
spend16 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend17 = Spend("Rent", 600, "Rent", "", "Debit")
spend18 = Spend("Party", 200, "Party", "", "Debit")
spend19 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend20 = Spend("Rent", 600, "Rent", "", "Debit")
spend21 = Spend("Party", 200, "Party", "", "Debit")
spend22 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend23 = Spend("Rent", 600, "Rent", "", "Debit")
spend24 = Spend("Party", 200, "Party", "", "Debit")
spend25 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend26 = Spend("Rent", 600, "Rent", "", "Debit")
spend27 = Spend("Party", 200, "Party", "", "Debit")
spend28 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend29 = Spend("Rent", 600, "Rent", "", "Debit")
spend30 = Spend("Party", 200, "Party", "", "Debit")
spend31 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend32 = Spend("Rent", 600, "Rent", "", "Debit")
spend33 = Spend("Party", 200, "Party", "", "Debit")
spend34 = Spend("Groceries", 200, "Groceries", "", "Debit")
spend35 = Spend("Rent", 600, "Rent", "", "Debit")
spend36 = Spend("Party", 200, "Party", "", "Debit")

spend37 = Spend("Car Damanges", 400, "Car", "", "Debit")
spend38 = Spend("Ticket", 200, "Ticket", "", "Debit")
spend39 = Spend("Doctor", 500, "Health", "", "Debit")


person = Person("Jacob", {}, {}, 1200)

income = Income("Work", 1400, "Work", "", "Debit")
income2 = Income("Work", 1400, "Work", "", "Debit")
income3 = Income("Work", 1400, "Work", "", "Debit")
income4 = Income("Work", 1400, "Work", "", "Debit")
income5 = Income("Work", 1400, "Work", "", "Debit")
income6 = Income("Work", 1400, "Work", "", "Debit")
income7 = Income("Work", 1400, "Work", "", "Debit")
income8 = Income("Work", 1400, "Work", "", "Debit")
income9 = Income("Work", 1400, "Work", "", "Debit")
income10 = Income("Work", 1400, "Work", "", "Debit")
income11 = Income("Work", 1400, "Work", "", "Debit")
income12 = Income("Work", 1400, "Work", "", "Debit")


income17 = Income("Birthday", 200, "Gift", "", "Cash")
income18 = Income("Raffle", 20, "Gift", "", "Venmo")
income19 = Income("Fantasy Football", 50, "Gift", "", "Venmo")
income20 = Income("March Madness", 75, "Gift", "", "Venmo")
income21 = Income("Christmas", 100, "Gift", "", "Cash")



person.add_income(income, datetime.date(2022, 1, 1))
person.add_income(income2, datetime.date(2022, 2, 1))
person.add_income(income3, datetime.date(2022, 3, 1))
person.add_income(income4, datetime.date(2022, 4, 3))
person.add_income(income5, datetime.date(2022, 5, 1))
person.add_income(income6, datetime.date(2022, 6, 3))
person.add_income(income7, datetime.date(2022, 7, 1))
person.add_income(income8, datetime.date(2022, 8, 3))
person.add_income(income9, datetime.date(2022, 9, 1))
person.add_income(income10, datetime.date(2022, 10, 3))
person.add_income(income11, datetime.date(2022, 11, 1))
person.add_income(income12, datetime.date(2022, 12, 3))
person.add_income(income17, datetime.date(2022, 6, 20))
person.add_income(income18, datetime.date(2022, 8, 15))
person.add_income(income19, datetime.date(2022, 3, 15))
person.add_income(income20, datetime.date(2022, 3, 7))
person.add_income(income21, datetime.date(2022, 12, 25))




person.add_spending(spend, datetime.date(2022, 1, 10))
person.add_spending(spend2, datetime.date(2022, 1, 15))
person.add_spending(spend3, datetime.date(2022, 1, 17))
person.add_spending(spend4, datetime.date(2022, 2, 20))
person.add_spending(spend5, datetime.date(2022, 2, 15))
person.add_spending(spend6, datetime.date(2022, 2, 17))
person.add_spending(spend7, datetime.date(2022, 3, 10))
person.add_spending(spend8, datetime.date(2022, 3, 15))
person.add_spending(spend9, datetime.date(2022, 3, 17))
person.add_spending(spend10, datetime.date(2022, 4, 10))
person.add_spending(spend11, datetime.date(2022, 4, 15))
person.add_spending(spend12, datetime.date(2022, 4, 17))
person.add_spending(spend13, datetime.date(2022, 5, 10))
person.add_spending(spend14, datetime.date(2022, 5, 15))
person.add_spending(spend15, datetime.date(2022, 5, 17))
person.add_spending(spend16, datetime.date(2022, 6, 10))
person.add_spending(spend17, datetime.date(2022, 6, 15))
person.add_spending(spend18, datetime.date(2022, 6, 17))
person.add_spending(spend19, datetime.date(2022, 7, 10))
person.add_spending(spend20, datetime.date(2022, 7, 15))
person.add_spending(spend21, datetime.date(2022, 7, 17))
person.add_spending(spend22, datetime.date(2022, 8, 10))
person.add_spending(spend23, datetime.date(2022, 8, 15))
person.add_spending(spend24, datetime.date(2022, 8, 17))
person.add_spending(spend25, datetime.date(2022, 9, 10))
person.add_spending(spend26, datetime.date(2022, 9, 15))
person.add_spending(spend27, datetime.date(2022, 9, 17))
person.add_spending(spend28, datetime.date(2022, 10, 10))
person.add_spending(spend29, datetime.date(2022, 10, 15))
person.add_spending(spend30, datetime.date(2022, 10, 17))
person.add_spending(spend31, datetime.date(2022, 11, 10))
person.add_spending(spend32, datetime.date(2022, 11, 15))
person.add_spending(spend33, datetime.date(2022, 11, 17))
person.add_spending(spend34, datetime.date(2022, 12, 10))
person.add_spending(spend35, datetime.date(2022, 12, 15))
person.add_spending(spend36, datetime.date(2022, 12, 17))
person.add_spending(spend37, datetime.date(2022, 10, 27))
person.add_spending(spend38, datetime.date(2022, 2, 9))
person.add_spending(spend39, datetime.date(2022, 12, 29))


print("Income: ",person.get_total_income())
print("Monthly December Income: ", person.get_total_monthly_income(12, 2022))
print("Spending: ",person.get_total_spending()) 
print("Balance: ", person.get_total_difference())
print(person.get_trend_monthly_income(12, 2022))
print(person.get_trend_monthly_income(1, 2022))
print(person.get_trend_yearly_income(2022))
print(person.get_trend_monthly_spend(12, 2022))
print(person.get_trend_monthly_spend(1, 2022))
print("Work income for one day:", person.get_categorical_day_income("Work", datetime.date(2022, 12, 3)))
print("Health spend for one day:", person.get_categorical_day_spend("Health", datetime.date(2022, 12, 29)))
print("Groceries spend in one month:", person.get_categorical_monthly_spending("Groceries", 12, 2022))
print("Work income for one month:", person.get_categorical_monthly_income("Work", 12, 2022))
print("Work income for a year:", person.get_categorical_yearly_income("Work", 2022))
print("Groceries spend for a year:", person.get_categorical_yearly_spend("Groceries", 2022))
print("Work income for all time:", person.get_total_categorical_income("Work"))
print("Groceries spend for all time:", person.get_total_categorical_spend("Groceries"))
print("Groceries spend over a time period:", person.get_categorical_x_spending("Groceries", 40, datetime.date(2022, 12, 4)))
print("Work income over a time period:", person.get_categorical_x_income("Work", 20, datetime.date(2022, 11, 19)))

print("Categorical yearly income:", person.get_yearly_income_by_category(2022))
print("Categorical yearly spend:", person.get_yearly_spend_by_category(2022))

# print(person.get_x_spending(10, ))

person.delete_income(income, datetime.date(2022, 12, 1))
print(person.get_trend_monthly_income(12, 2022))
person.delete_income(spend, datetime.date(2022, 12, 5))
print(person.get_trend_monthly_spend(12, 2022))
print(person.get_trend_yearly_income(2022))
print(person.get_trend_monthly_difference(12, 2022))