function filterTrade() {
  //Gets all the data from the form
  var tradeID = document.getElementById("tradeID").value;
  var datePlaced = document.getElementById("datePlace").value;
  var dateMature = document.getElementById("maturityDate").value;
  var product = document.getElementById("product").value;
  var quantity = document.getElementById("quantity").value;
  var buying = document.getElementById("buyingParty").value;
  var selling = document.getElementById("sellingParty").value;
  var notionalCurr = document.getElementById("currenyNotional").value;
  var notionalPrice = document.getElementById("priceNotional").value;
  var underCurr = document.getElementById("currenyUnder").value;
  var underPrice = document.getElementById("priceUnder").value;
  var strikePrice = document.getElementById("strikePrice").value;

  // Set up our HTTP request
var xhr = new XMLHttpRequest();

// Setup our listener to process completed requests
xhr.onreadystatechange = function () {
  var DONE = 4; // readyState 4 means the request is done.
  var OK = 200; // status 200 is a successful return.
  if (xhr.readyState === DONE) {
    if (xhr.status === OK) {
      //Updates the show more button
      var button = document.getElementById("showMoreButton");
      button.setAttribute('onclick',"showMoreTrades('"+datePlaced + "',10)");
      button.innerHTML = "Show More"

      //Adds the trades to the table
      var trades = JSON.parse(xhr.response);
      var tableBody = document.getElementById("transBody");
      var table = document.getElementById("transTable");
      tableBody.innerHTML = ""; //Remove all old trades
      var trade;

      if (trades.length > 0) {
        table.style.display = "table";
      } else {
        button.innerHTML = "No Trades To Show";
        table.style.display = "none";
      }
       //Remove all old trades
      for (tradeNum in trades) {
        trade = trades[tradeNum];
        //New row
        var newRow = tableBody.insertRow(-1);
        newRow.setAttribute('onclick', "window.location.href='alter-trade.php?tradeID="+trade["tradeID"]+"'");

        //New cells
        var newCell = newRow.insertCell(0);
        var newText = document.createTextNode(trade["datePlaced"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(1);
        newText = document.createTextNode(trade["product"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(2);
        newText = document.createTextNode(trade["tradeID"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(3);
        newText = document.createTextNode(trade["buyingParty"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(4);
        newText = document.createTextNode(trade["sellingParty"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(5);
        newText = document.createTextNode(trade["notionalPrice"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(6);
        newText = document.createTextNode(trade["quantity"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(7);
        newText = document.createTextNode(trade["notionalCurrency"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(8);
        newText = document.createTextNode(trade["maturityDate"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(9);
        newText = document.createTextNode(trade["underlyingPrice"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(10);
        newText = document.createTextNode(trade["underlyingCurrency"]);
        newCell.appendChild(newText);

        newCell = newRow.insertCell(11);
        newText = document.createTextNode(trade["strikePrice"]);
        newCell.appendChild(newText);
      }
      //Close the filter menu
      document.getElementById("content").style.display= "none";
    } else {
      alert('Error: ' + xhr.status); // An error occurred contentduring the request.
    }
  }
};

// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
var URL = "http://localhost:5002/filterTrades/0";

URL = generateURL(URL, tradeID);
URL = generateURL(URL, datePlaced);
URL = generateURL(URL, dateMature);
URL = generateURL(URL, product);
URL = generateURL(URL, quantity);
URL = generateURL(URL, buying);
URL = generateURL(URL, selling);
URL = generateURL(URL, notionalCurr);
URL = generateURL(URL, notionalPrice);
URL = generateURL(URL, underCurr);
URL = generateURL(URL, underPrice);
URL = generateURL(URL, strikePrice);

xhr.open('GET', URL, true);
xhr.send();

}

function generateURL(url, field) {
  if (field != "") {
    url += "/" + field;
  } else {
    url += "/null";
  }
  return url
}
