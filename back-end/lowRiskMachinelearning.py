import numpy as np
import statsmodels.api as sm
import datetime as DT
from datetime import date
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

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123password", database="bankDB", allow_local_infile="True")
mycursor = mydb.cursor()
mycursor.execute("SET GLOBAL local_infile = 1; ")
mycursor.execute("LOAD DATA LOCAL INFILE '/Users/colinlam88/Downloads/Low_Risk.csv' INTO TABLE trades FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8,@col9,@col10,@col11,@col12) set dateofTrade=STR_TO_DATE(@col1, '%d/%m/%Y %l:%i:%s'), tradeID=@col2, name=@col3, buyingParty=@col4, sellingParty=@col5, notionalAmount=@col6, notionalCurrency=@col7, quantity=@col8, maturity=STR_TO_DATE(@col9, '%d/%m/%Y'), underlyingPrice=@col10, underlyingCurrency=@col11, strikePrice=@col12; ")
mydb.commit()

mycursor = mydb.cursor()
mycursor.execute("SET GLOBAL local_infile = 1; ")
mycursor.execute("SELECT maturity, strikePrice, underlyingPrice, notionalAmount FROM trades WHERE buyingParty = 'AWYB85' ;")
myresult = mycursor.fetchall()


currentDate = []
maturityDate = []
strikePrice = []
underlyingPrice = []
notionalAmount = []

for attribute in myresult:
    maturityDate.append(attribute[0])
    strikePrice.append(attribute[1])
    underlyingPrice.append(attribute[2])
    notionalAmount.append(attribute[3])

count3 = 0
for convert in strikePrice:
    print(count3)
    strikePrice[count3] = int(convert)
    count3 +=1

count4 = 0
for convert in underlyingPrice:
    underlyingPrice[count4] = int(convert)
    count4 +=1

count5 = 0
for convert in notionalAmount:
    notionalAmount[count5] = int(convert)
    count5 +=1

print("Underlying Price: " , underlyingPrice)
print("Strike Price: " , strikePrice)
print("Notional amount: " , notionalAmount)



class BuyerModel:
    def _init_(self):
        pass

    x = []
    y = []
    sensitivity = 0.7

    def addData(self, maturityDate, strike, underlying, notional):
        currentDate = datetime.date(2010, 1, 1)
        dateDifference = maturityDate - currentDate
        time = dateDifference.days
        strikeUnderlyingChange = abs((strike - underlying)/underlying)
        self.x.append([strikeUnderlyingChange, time])
        self.y.append(notional)
        return True

    def createModel(self):
        self.x, self.y = np.array(self.x), np.array(self.y)
        self.x = sm.add_constant(self.x)
        model = sm.OLS(self.y, self.x)
        results = model.fit()
        print(results.summary())
        print('predicted response:', results.predict(self.x), sep='\n')
        return results

    def raiseFlag(self, underlying, strike, time, notional):
        results = self.createModel()
        strikeUnderlyingChange = abs((strike - underlying)/underlying)
        inputsX = [strikeUnderlyingChange, time, 1, 2]         # 1 and 2 are just dummies
        x_new = sm.add_constant(np.reshape(inputsX, (-1, 2)))
        print("x_new = ", x_new)
        y_new = results.predict(x_new)
        print("y_new = ", y_new[0])
        if (notional > y_new[0]*(1-self.sensitivity)  and notional < y_new[0]*(self.sensitivity+1)) == True:
            return True
        return False

    def changeSensitivity(self, sensitivity):
        self.sensitivity = sensitivity


test = BuyerModel()
count2 = 0
while count2 < len(myresult):
    test.addData(maturityDate[count2], strikePrice[count2], underlyingPrice[count2], notionalAmount[count2])
    count2 +=1

print("test.x = ", test.x)
print("test.y = ", test.y)
print(test.raiseFlag(656, 144, 285, 20000))
