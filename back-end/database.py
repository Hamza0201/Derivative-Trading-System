import mysql.connector
from datetime import datetime as dt
import csv
import string
import random
import learning as learning

FILEPATH = "../cs261dummydata"

def createConnection():
    mydb = mysql.connector.connect(host="localhost", user="root", passwd="password123", database="bankDB", allow_local_infile="True")
    mycursor = mydb.cursor()
    return mydb, mycursor

def createSchema():
    mydb, mycursor = createConnection()
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
    mycursor.execute("CREATE TABLE trades (dateOfTrade DATETIME NOT NULL,tradeID VARCHAR(255) NOT NULL,name VARCHAR(255),buyingParty VARCHAR(255),sellingParty VARCHAR(255),notionalAmount NUMERIC,quantity INTEGER,notionalCurrency VARCHAR(3),maturity DATE,underlyingPrice NUMERIC,underlyingCurrency VARCHAR(3),strikePrice NUMERIC,PRIMARY KEY (tradeID),FOREIGN KEY (buyingParty)REFERENCES companyCodes (tradingID),FOREIGN KEY (sellingParty)REFERENCES companyCodes (tradingID),FOREIGN KEY (notionalCurrency)REFERENCES currencyValues (currency),FOREIGN KEY (underlyingCurrency)REFERENCES currencyValues (currency),CHECK (quantity > 0));")
    mydb.commit()
    mydb.close()

def loadDataset():
    mydb, mycursor = createConnection()
    mycursor.execute("SET GLOBAL local_infile = 1; ")
    mycursor.execute("LOAD DATA LOCAL INFILE '{0}/companyCodes.csv' INTO TABLE companyCodes FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (@col1,@col2) set name=@col1, tradingID=@col2; ".format(FILEPATH))
    mycursor.execute("LOAD DATA LOCAL INFILE '{0}/productSellers.csv' INTO TABLE productSellers FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 ROWS (@col1,@col2) set productName=@col1, companyID=@col2; ".format(FILEPATH))
    mycursor.execute("LOAD DATA LOCAL INFILE '{0}/currencyValues/2019/April/02042019.csv' INTO TABLE currencyValues FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (@col1,@col2,@col3) set dateofTrade=STR_TO_DATE(@col1, '%d/%m/%Y'), currency=@col2, valueInUSD=@col3; ".format(FILEPATH))
    mycursor.execute("LOAD DATA LOCAL INFILE '{0}/derivativeTrades/2019/April/02042019.csv' INTO TABLE trades FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8,@col9,@col10,@col11,@col12) set dateofTrade=STR_TO_DATE(@col1, '%d/%m/%Y'), tradeID=@col2, name=@col3, buyingParty=@col4, sellingParty=@col5, notionalAmount=@col6, notionalCurrency=@col7, quantity=@col8, maturity=STR_TO_DATE(@col9, '%d/%m/%Y'), underlyingPrice=@col10, underlyingCurrency=@col11, strikePrice=@col12 ; ".format(FILEPATH))
    mycursor.execute("LOAD DATA LOCAL INFILE '{0}/derivativeTrades/testData/High_Risk.csv' INTO TABLE trades FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8,@col9,@col10,@col11,@col12) set dateofTrade=STR_TO_DATE(@col1, '%d/%m/%Y'), tradeID=@col2, name=@col3, buyingParty=@col4, sellingParty=@col5, notionalAmount=@col6, notionalCurrency=@col7, quantity=@col8, maturity=STR_TO_DATE(@col9, '%d/%m/%Y'), underlyingPrice=@col10, underlyingCurrency=@col11, strikePrice=@col12 ; ".format(FILEPATH))
    mycursor.execute("LOAD DATA LOCAL INFILE '{0}/derivativeTrades/testData/Low_Risk.csv' INTO TABLE trades FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 ROWS (@col1,@col2,@col3,@col4,@col5,@col6,@col7,@col8,@col9,@col10,@col11,@col12) set dateofTrade=STR_TO_DATE(@col1, '%d/%m/%Y'), tradeID=@col2, name=@col3, buyingParty=@col4, sellingParty=@col5, notionalAmount=@col6, notionalCurrency=@col7, quantity=@col8, maturity=STR_TO_DATE(@col9, '%d/%m/%Y'), underlyingPrice=@col10, underlyingCurrency=@col11, strikePrice=@col12 ; ".format(FILEPATH))
    mydb.commit()
    mydb.close()

def addTrade(tradeID, productID, buyingParty, sellingParty, notionalVal, notionalCurrency, quantity, maturityDate, underlyingPrice, underlyingCurrency, strikePrice):
        warning = {}
        notionalVal = int(notionalVal)
        quantity = int(quantity)
        underlyingPrice = int(underlyingPrice)
        strikePrice = int(strikePrice)
        datePlaced = dt.now()
        datePlaced.strftime('%Y-%m-%d %H:%M:%S')
        valid = validTrade(tradeID, productID, buyingParty, sellingParty, notionalVal, notionalCurrency, quantity, maturityDate, underlyingPrice, underlyingCurrency, strikePrice, datePlaced)
        if valid == "":
            try:
                ID = id_generator()
                flag, lower, upper = learning.checkDetails(buyingParty, dt.strptime(maturityDate, '%Y-%m-%d'), datePlaced, strikePrice, underlyingPrice, notionalVal)
                if flag:
                    warning = {'tradeID': ID, 'notionalVal': notionalVal, 'predictedLower': lower, 'predictedUpper': upper}

                mydb, mycursor = createConnection()
                sqlFormula = "INSERT INTO trades (dateOfTrade, tradeID, maturity, buyingParty, sellingParty, name, quantity, notionalCurrency, notionalAmount, underlyingCurrency, underlyingPrice, strikePrice) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                tradeDetails = (datePlaced, ID, maturityDate, buyingParty, sellingParty, productID, quantity, notionalCurrency, notionalVal, underlyingCurrency, underlyingPrice, strikePrice)
                mycursor.execute(sqlFormula, tradeDetails)
                mydb.commit()
                mydb.close()
                return "Trade successfully entered.", warning
            except:
                return "SQL error processing trade entry.", {}
        else:
            return valid, warning


def alterTrade(tradeID, productID='', buyingParty='', sellingParty='', notionalVal='', notionalCurrency='', quantity='', maturityDate='', underlyingPrice='', underlyingCurrency='', strikePrice=''):
    if notionalVal != '':
        notionalVal = int(notionalVal)
    if quantity != '':
        quantity = int(quantity)
    if underlyingPrice != '':
        underlyingPrice = int(underlyingPrice)
    if strikePrice != '':
        strikePrice = int(strikePrice)
    datePlaced = dt.now()
    datePlaced.strftime('%Y-%m-%d')
    valid = validTrade(tradeID, productID, buyingParty, sellingParty, notionalVal, notionalCurrency, quantity, maturityDate, underlyingPrice, underlyingCurrency, strikePrice, datePlaced)
    if valid != '':
        return valid
    try:
        if tradeExists(tradeID):
            mydb, mycursor = createConnection()
            sqlInput = "SELECT * FROM trades WHERE tradeID = %s; "
            mycursor.execute(sqlInput, (tradeID,))
            for row in mycursor.fetchall():
                temp = row[0]
            if (temp.strftime('%Y-%m-%d')) == (datePlaced.strftime('%Y-%m-%d')):
                sqlFormula = "UPDATE trades SET `maturity` = (CASE WHEN %s = '' THEN `maturity` ELSE STR_TO_DATE(%s, '%Y-%m-%d') END), `buyingParty` = (CASE WHEN %s = '' THEN `buyingParty` ELSE %s END), `sellingParty` = (CASE WHEN %s = '' THEN `sellingparty` ELSE %s END), `name` = (CASE WHEN %s = '' THEN `name` ELSE %s END), `quantity` = (CASE WHEN %s = '' THEN `quantity` ELSE %s END), `notionalCurrency` = (CASE WHEN %s = '' THEN `notionalCurrency` ELSE %s END), `underlyingCurrency` = (CASE WHEN %s = '' THEN `underlyingCurrency` ELSE %s END), `strikePrice` = (CASE WHEN %s = '' THEN `strikePrice` ELSE %s END) WHERE `tradeID` = %s; "
                mycursor.execute(sqlFormula, (maturityDate, maturityDate, buyingParty, buyingParty, sellingParty, sellingParty, productID, productID, quantity, quantity, notionalCurrency, notionalCurrency, underlyingCurrency, underlyingCurrency, strikePrice, strikePrice, tradeID))
                mydb.commit()
                mydb.close()
                return "Trade successfully altered."
            else:
                mydb.close()
                return "You cannot edit trades that were entered on a different day."
        else:
            return "Trade does not exist."
    except:
        return "SQl error occurred when altering trade."

def getTrade(tradeID):
    if tradeExists(tradeID):
        mydb, mycursor = createConnection()
        sqlInput = "SELECT * FROM trades WHERE tradeID = %s; "
        mycursor.execute(sqlInput, (tradeID,))
        for row in mycursor.fetchall():
            mydb.close()
            return {'tradeID': row[1], 'product': row[2], 'buyingParty': row[3],
                        'sellingParty': row[4], 'notionalCurrency': row[7], 'quantity': row[6],
                        'notionalPrice': float(row[5]) , 'datePlaced': row[0].strftime('%Y-%m-%d'), 'maturityDate': row[8].strftime('%Y-%m-%d'),
                        'underlyingPrice': float(row[9]), 'underlyingCurrency':row[10] , 'strikePrice': float(row[11])}
    else:
        return "Trade does not exist"

def filterTrades(topTradeNum='0', tradeID='null', datePlaced='null', matureDate='null', product='null', quantity='null', buying='null', selling='null', notCur='null', notPrice='null', unCur='null', unPrice='null', strike='null'):
    condition = ""
    variables = []
    if tradeID != 'null':
        condition += "tradeID = %s AND "
        variables.append(tradeID)
    if datePlaced != 'null':
        condition += "DATE(dateOfTrade) = %s AND "
        dt.strptime(datePlaced, '%Y-%m-%d')
        variables.append(datePlaced)
    if matureDate != 'null':
        condition += "maturity = %s AND "
        dt.strptime(matureDate, '%Y-%m-%d')
        variables.append(matureDate)
    if product != 'null':
        condition += "name = %s AND "
        variables.append(product)
    if quantity != 'null':
        condition += "quantity = %s AND "
        variables.append(quantity)
    if buying != 'null':
        condition += "buyingParty = %s AND "
        variables.append(buying)
    if selling != 'null':
        condition += "sellingParty = %s AND "
        variables.append(selling)
    if notCur != 'null':
        condition += "notionalCurrency = %s AND "
        variables.append(notCur)
    if notPrice != 'null':
        condition += "notionalAmount = %s AND "
        variables.append(notPrice)
    if unPrice != 'null':
        condition += "underlyingPrice = %s AND "
        variables.append(unPrice)
    if strike != 'null':
        condition += "strikePrice = %s AND "
        variables.append(strike)
    if condition == "":
        return []
    condition = condition[:-5] + " "
    mydb, mycursor = createConnection()
    sqlInput = "SELECT * FROM trades WHERE " + condition + "limit "+ topTradeNum +", 10;"
    mycursor.execute(sqlInput, variables)
    trades = []
    for row in mycursor.fetchall():
        trades.append({'tradeID': row[1], 'product': row[2], 'buyingParty': row[3],
                        'sellingParty': row[4], 'notionalCurrency': row[7], 'quantity': row[6],
                        'notionalPrice': float(row[5]) , 'datePlaced': row[0].strftime('%Y-%m-%d'), 'maturityDate': row[8].strftime('%Y-%m-%d'),
                        'underlyingPrice': float(row[9]), 'underlyingCurrency':row[10] , 'strikePrice': float(row[11])})
    mydb.close()
    return trades

def getAllTrades(date):
    try:
        dt.strptime(date, '%Y-%m-%d')
    except:
        return "Invalid date given"
    mydb, mycursor = createConnection()
    sqlInput = "SELECT * FROM trades WHERE DATE(dateOfTrade) = %s ; "
    mycursor.execute(sqlInput, (date,))
    trades = []
    for row in mycursor.fetchall():
        trades.append({'tradeID': row[1], 'product': row[2], 'buyingParty': row[3],
                        'sellingParty': row[4], 'notionalCurrency': row[7], 'quantity': row[6],
                        'notionalPrice': float(row[5]) , 'datePlaced': row[0].strftime('%Y-%m-%d'), 'maturityDate': row[8].strftime('%Y-%m-%d'),
                        'underlyingPrice': float(row[9]), 'underlyingCurrency':row[10] , 'strikePrice': float(row[11])})
    mydb.close()
    return trades

def getCurrencies():
    mydb, mycursor = createConnection()
    sqlInput = "SELECT currency FROM currencyValues; "
    mycursor.execute(sqlInput)
    currencies = []
    for row in mycursor.fetchall():
        currencies.append(row[0])
    mydb.close()
    return currencies

def deleteTrade(tradeID):
    now = dt.now()
    if tradeExists(tradeID):
        mydb, mycursor = createConnection()
        sqlInput = "SELECT * FROM trades WHERE tradeID = %s; "
        mycursor.execute(sqlInput, (tradeID,))
        for row in mycursor.fetchall():
            temp = row[0]
        if (temp.strftime('%Y-%m-%d')) == (now.strftime('%Y-%m-%d')):
            sqlFormula = "DELETE FROM `trades` WHERE `tradeID` = %s; "
            mycursor.execute(sqlFormula, (tradeID,))
            mydb.commit()
            mydb.close()
            return "Trade Successfully deleted."
        else:
            mydb.close()
            return "Cannot delete trade from previous days."
    else:
        return "Trade does not exist."

def id_generator(size=16, chars=string.ascii_uppercase, chars2=string.digits):
    letters = ''.join(random.choice(chars) for _ in range(8))
    digits = ''.join(random.choice(chars2) for _ in range(8))
    return (letters + digits)

def validTrade(tradeID, productID, buyingParty, sellingParty, notionalVal, notionalCurrency, quantity, maturityDate, underlyingPrice, underlyingCurrency, strikePrice, datePlaced):
    if not validParty(buyingParty):
        return "Invalid buying party identifier given."
    if not validParty(sellingParty):
        return "Invalid selling party identifier given."
    if not validValue(quantity):
        return "Invalid quantity given."
    if not validCurrency(notionalCurrency):
        return "Invalid notional currency given."
    if not validValue(notionalVal):
        return "Invalid notional value given."
    if not validCurrency(underlyingCurrency):
        return "Invalid underlying currency given."
    if not validValue(underlyingPrice):
        return "Invalid underlying price given."
    if not validValue(strikePrice):
        return "Invalid strike price given."
    if not validDate(datePlaced, maturityDate):
        return "Invalid maturity date given."
    return ""

def validValue(value):
    if value == '' or value > 0:
        return True
    else:
        return False

def validDate(datePlaced, maturityDate):
    if maturityDate == '':
        return True
    try:
        maturityDate = dt.strptime(maturityDate, '%Y-%m-%d')
        return maturityDate >= datePlaced
    except ValueError:
        return False

def tradeExists(tradeID):
    mydb, mycursor = createConnection()
    sqltradeID = "SELECT tradeID from trades;"
    mycursor.execute(sqltradeID)
    exists = False
    for row in mycursor.fetchall():
        if row[0] == tradeID:
            exists = True
    mydb.close()
    return exists

def validParty(party):
    if party == '':
        return True
    mydb, mycursor = createConnection()
    sqlInput = "SELECT tradingID FROM companyCodes; "
    mycursor.execute(sqlInput)
    exists = False
    for row in mycursor.fetchall():
        if row[0] == party:
            exists = True
    mydb.close()
    return exists

def validCurrency(currency):
    if currency == '':
        return True
    if not currency.isalnum() and len(currency) != 3:
        return False
    mydb, mycursor = createConnection()
    sqlInput = "SELECT currency FROM currencyValues; "
    mycursor.execute(sqlInput)
    exists = False
    for row in mycursor.fetchall():
        if row[0] == currency:
            exists = True
    mydb.close()
    return exists

def getReport(date):
    try:
        dt.strptime(date, '%d%m%Y')
    except ValueError:
        return "Date must be in format (DDMMYYYY)"

    d = dt.strptime(date[2:4], '%m')
    if os.path.exists('{0}/reports'.format(FILEPATH) + date[4:9] + "/" + d.strftime('%b') + "/" + date + '.csv'):
        with open('{0}/reports/'.format(FILEPATH) + date[4:9] + "/" + d.strftime('%b') + "/" + date + '.csv', 'r') as file:
            reader = csv.reader(file)
            return reader
    else:
        return "Report does not exist."

if __name__ == "__main__":
    createSchema()
    loadDataset()
