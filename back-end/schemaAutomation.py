import mysql.connector
from datetime import datetime
import schedule
import time
import shutil

mydb = mysql.connector.connect(host="localhost", user="root", passwd="password123", database="bankDB", allow_local_infile="True")
mycursor = mydb.cursor()

def job():
    mycursor.execute("SET foreign_key_checks = 0;")
    mycursor.execute("DROP TABLE IF EXISTS `products`;")
    mycursor.execute("DROP TABLE IF EXISTS `companyCodes`;")
    mycursor.execute("DROP TABLE IF EXISTS `currencyValues`;")
    mycursor.execute("DROP TABLE IF EXISTS `productSellers`;")
    mycursor.execute("DROP TABLE IF EXISTS `productPrices`;")
    mycursor.execute("DROP TABLE IF EXISTS `stockPrices`;")
    mycursor.execute("DROP TABLE IF EXISTS `trades`;")
    mycursor.execute("SET foreign_key_checks = 1;")
    mycursor.execute("CREATE TABLE companyCodes (tradingID VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL,PRIMARY KEY (tradingID));")
    mycursor.execute("CREATE TABLE currencyValues (currency CHAR(3) NOT NULL,dateofTrade DATE NOT NULL,valueInUSD DECIMAL(15,4),PRIMARY KEY (currency , dateofTrade));")
    mycursor.execute("CREATE TABLE productSellers (productName VARCHAR(255) NOT NULL,companyID VARCHAR(255) NOT NULL,PRIMARY KEY (productName , companyID), FOREIGN KEY (companyID) REFERENCES companyCodes (tradingID));")
    mycursor.execute("CREATE TABLE productPrices (name VARCHAR(255) NOT NULL,dateofTrade DATE NOT NULL,marketPrice NUMERIC,PRIMARY KEY (name , dateofTrade),FOREIGN KEY (name)REFERENCES productSellers (productName));")
    mycursor.execute("CREATE TABLE stockPrices (companyID VARCHAR(255) NOT NULL,dateofTrade DATE NOT NULL,stockPrices NUMERIC,PRIMARY KEY (companyID , dateofTrade),FOREIGN KEY (companyID)REFERENCES companyCodes (tradingID));")
    mycursor.execute("CREATE TABLE trades (dateOfTrade DATETIME NOT NULL,tradeID VARCHAR(255) NOT NULL,name VARCHAR(255),buyingParty VARCHAR(255),sellingParty VARCHAR(255),quantity INTEGER,notionalCurrency VARCHAR(3), notionalAmount DECIMAL(20,2),maturity DATE,underlyingPrice DECIMAL(20,2),underlyingCurrency VARCHAR(3),strikePrice DECIMAL(20,2),PRIMARY KEY (tradeID),FOREIGN KEY (buyingParty)REFERENCES companyCodes (tradingID),FOREIGN KEY (sellingParty)REFERENCES companyCodes (tradingID),FOREIGN KEY (notionalCurrency)REFERENCES currencyValues (currency),FOREIGN KEY (underlyingCurrency)REFERENCES currencyValues (currency),CHECK (quantity > 0));")
    mydb.commit()

schedule.every().day.at("23:59").do(job)
while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
