import mysql.connector
import datetime
from datetime import datetime as dt
import sys
import csv
import string
import random
import os
import csv
import validate
from decimal import Decimal

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123password",
    database="bankDB",
    allow_local_infile="True"
)

companyTradeID = []
first_char_company = []
second_char_company = []
third_char_company =[]
last_char_company =[]
last_number_company = []
sellingParty = []


mycursor = mydb.cursor()

mycursor.execute("SET GLOBAL local_infile = 1; ")

mycursor.execute("SELECT tradingID FROM companyCodes ;")

myresult = mycursor.fetchall()

for attribute in myresult:
    companyTradeID.append(attribute[0])

print(companyTradeID)

for attribute in myresult:
    s = attribute[0]
    first_char_company.append(s[0:4])

print(first_char_company)

for attribute in myresult:
    s = attribute[0]
    second_char_company.append(s[0:3])

print(second_char_company)

for attribute in myresult:
    s = attribute[0]
    third_char_company.append(s[0:2])

print(third_char_company)

for attribute in myresult:
    s = attribute[0]
    last_char_company.append(s[1:4])

print(last_char_company)

for attribute in myresult:
    s = attribute[0]
    last_number_company.append(s[2:6])

print(last_number_company)


test = "YTBH13"      #can be deleted

#****************PLEASE SEE THESE FUNCTIONS TO UNDERSTAND THE PROGRAM*************************
def checkParty(input):
    if not input in companyTradeID:
        first_char = input[0:4]
        second_char = input[0:3]
        third_char = input[0:2]
        last_char = input[1:4]
        last_number = input[2:6]
        if first_char in first_char_company:
            y = first_char_company.index(first_char)   #first four characters
            x = companyTradeID[y]
            print("Do you mean " + x + "?")
            return False

        elif second_char in second_char_company:        #first three characters
            y = second_char_company.index(second_char)
            x = companyTradeID[y]
            print("Do you mean " + x + "?")
            return False

        elif third_char in third_char_company:          #first two characters
            y = third_char_company.index(third_char)
            x = companyTradeID[y]
            print("Do you mean " + x + "?")
            return False
        elif last_char in last_char_company:
            y = last_char_company.index(last_char)
            x = companyTradeID[y]
            print("Do you mean " + x + "?")
            return False
        elif last_number in last_number_company:
            y = last_number_company.index(last_number)
            x = companyTradeID[y]
            print("Do you mean " + x + "?")
            return False
        else: print("Invaild companyTradeID input")
        return False
    else: print("No error")
    return True


checkParty(test)
