from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify
import database as db

app = Flask(__name__)
api = Api(app)

#Hard code machine learning control
trainingMode = False
warningRules = []

#To put an database result into json use jsonify(result)

#Basic Test
@app.route('/', methods=['GET'])
def test():
    return "API is working"

#Trades
@app.route('/getAllTrades/<string:date>', methods=['GET']) #Strings in the format YYYY-MM-DD
def getTrades(date, top):
    response = jsonify(db.getAllTrades(date))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#Get trades based on the fliters
@app.route('/filterTrades/<string:topTradeNum>/<string:tradeID>/<string:datePlaced>/<string:matureDate>/<string:product>/<string:quantity>/<string:buying>/<string:selling>/<string:notCur>/<string:notPrice>/<string:unCur>/<string:unPrice>/<string:strike>', methods=['GET'])
def filterTrades(topTradeNum='0', tradeID='', datePlaced='', matureDate='', product='', quantity='', buying='', selling='', notCur='', notPrice='', unCur='', unPrice='', strike=''):
    #will send null as the string if not filtering on it
    response = jsonify(db.filterTrades(topTradeNum, tradeID, datePlaced, matureDate, product, quantity, buying, selling, notCur, notPrice, unCur, unPrice, strike))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getTrade/<string:tradeID>', methods=['GET'])
def getTrade(tradeID):
    return jsonify(db.getTrade(tradeID))

@app.route('/deleteTrade', methods=['POST'])
def deleteTrade():
    data = request.form
    response = jsonify(db.deleteTrade(data['tradeID']))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/addTrade', methods=['POST'])
def addTrade():
    data = request.form
    result, warning = db.addTrade(data['tradeID'], data['product'], data['buyingParty'], data['sellingParty'], data['notionalPrice'], data['notionalCurrency'], data['quantity'], data['maturityDate'], data['underlyingPrice'], data['underlyingCurrency'], data['strikePrice'])
    if warning != {}:
        warningRules.append(warning)
    result = {'result': result, 'warning': warning }
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/alterTrade', methods=['POST'])
def alterTrade():
    data = request.form
    response = jsonify(db.alterTrade(data['tradeID'], data['product'], data['buyingParty'], data['sellingParty'], data['notionalPrice'], data['notionalCurrency'], data['quantity'], data['maturityDate'], data['underlyingPrice'], data['underlyingCurrency'], data['strikePrice']))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#Currencies
@app.route('/getCurrencies', methods=['GET'])
def getCurrencies():
    return jsonify(db.getCurrencies())

#Warning Rules
@app.route('/warningrules', methods=['GET'])
def getWarningRules():
    return jsonify(warningRules)

@app.route('/warningrules', methods=['POST'])
def deleteWarningRules():
    data = request.form
    i = 0
    for rule in warningRules:
        if data['tradeID'] == rule['tradeID'] and data['notionalVal'] == str(rule['notionalVal']) and data['predictedUpper'] == str(rule['predictedUpper']) and  data['predictedLower'] == str(rule['predictedLower']):
            del warningRules[i]
        i = i + 1
    response = jsonify("Rule deleted.")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#Training mode
@app.route('/trainingMode', methods=['GET'])
def getTrainingMode():
    return jsonify(trainingMode)

@app.route('/trainingMode', methods=['POST'])
def setTrainingMode():
    global trainingMode
    trainingMode = not(trainingMode)
    response = jsonify("updated")
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

#Report
@app.route('/getReport/<string:date>', methods=['GET'])
def getReport(date):
    return jsonify(db.getAllTrades(date))


#Main to run the API
if __name__ == '__main__':
     app.run(port='5002')
