from datetime import date
import mysql.connector
import numpy as np
from sklearn.linear_model import LinearRegression
import database as db

def checkDetails(buyingParty, maturityDate, currentDate, strike, underlying, notional):
    buyer = BuyerModel()
    mydb, mycursor = db.createConnection()
    sqlInput = "SELECT maturity, dateOfTrade, strikePrice, underlyingPrice, notionalAmount FROM trades WHERE buyingParty = %s AND dateOfTrade BETWEEN NOW() - INTERVAL 30 DAY AND NOW(); "
    mycursor.execute(sqlInput, (buyingParty, ))
    myresult = mycursor.fetchall()
    count = 0
    for attribute in myresult:
        count += 1
        buyer._addData(attribute[0], attribute[1].date(), float(attribute[2]), float(attribute[3]), float(attribute[4]))
    mydb.close()
    if count == 0:
        return False, 0, 0
    lower, upper = buyer._predict(maturityDate, currentDate, strike, underlying, notional)
    if lower < 0 and upper < 0:
        return False, 0, 0
    if lower < 0 and upper > 0:
        lower = 0
    return (notional < lower or notional > upper), round(lower, 2), round(upper, 2)

class BuyerModel:
    @staticmethod
    def __calcInfo(maturityDate, currentDate, strike, underlying):
        dateDifference = maturityDate - currentDate
        time = dateDifference.days
        strikeUnderlyingChange = abs((strike - underlying)/underlying)
        strikeUnderlyingChange, time
        return strikeUnderlyingChange, time

    def __init__(self):
        self.__x = []
        self.__y = []
        self.__sensitivity = 0.7

    def _addData(self, maturityDate, currentDate, strike, underlying, notional):
        strikeUnderlyingChange, time = BuyerModel.__calcInfo(maturityDate, currentDate, strike, underlying)
        self.__x.append([strikeUnderlyingChange, time])
        self.__y.append(notional)

    def __createModel(self):
        self.__x, self.__y = np.array(self.__x), np.array(self.__y)
        results = LinearRegression().fit(self.__x, self.__y)
        return results

    def _predict(self, maturityDate, currentDate, strike, underlying, notional):
        strikeUnderlyingChange, time = BuyerModel.__calcInfo(maturityDate, currentDate, strike, underlying)
        results = self.__createModel()
        inputsX = np.reshape([strikeUnderlyingChange, time], (1, -1))
        y_new = results.predict(inputsX)
        return y_new[0]*(1-self.__sensitivity), y_new[0]*(self.__sensitivity+1)

    def setSensitivity(self, sensitivity):
        self.__sensitivity = sensitivity
