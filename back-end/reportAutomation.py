import mysql.connector
from datetime import datetime
import sys
import csv
import string
import os
import schedule #Need to install python library - pip install schedule
import time
import shutil


FILEPATH = "../csvReports"
mydb = mysql.connector.connect(host="localhost", user="root", passwd="password123", database="bankDB", allow_local_infile="True")
mycursor = mydb.cursor()

def job():
    mycursor.execute("SELECT 'dateOfTrade', 'tradeID', 'name', 'buyingParty', 'sellingParty', 'notionalAmount', 'quantity', 'notionalCurrency', 'maturity', 'underlyingPrice', 'underlyingCurrency', 'strikePrice' UNION ALL SELECT DATE_FORMAT(dateOfTrade, '%d/%m/%Y %I:%i'), tradeID, name, buyingParty, sellingParty, notionalAmount, quantity, notionalCurrency, maturity, underlyingPrice, underlyingCurrency, strikePrice FROM TRADES INTO OUTFILE '{0}/new.csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n'; ".format(FILEPATH))
    mydb.commit()
    now = datetime.now()
    if not os.path.exists(FILEPATH + now.strftime('%Y')):
        os.mkdir(FILEPATH + now.strftime('%Y'))
    if not os.path.exists(FILEPATH + now.strftime('%Y') + "/" + now.strftime('%b')):
        os.mkdir(FILEPATH + now.strftime('%Y') + "/" + now.strftime('%b'))
    os.rename(FILEPATH+'/new.csv', FILEPATH + now.strftime('%d%m%Y') + '.csv')
    shutil.move(FILEPATH + now.strftime('%d%m%Y') + ".csv", FILEPATH + now.strftime('%Y') + "/" + now.strftime('%b') + "/" + now.strftime('%d%m%Y') + ".csv")

schedule.every().day.at("09:44").do(job)
while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
