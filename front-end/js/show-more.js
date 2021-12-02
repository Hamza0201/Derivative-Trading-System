function showMoreTrades(date, totalNumShown) {
  //Add 10 so that next time the button pressed it gets the next 10
  var button = document.getElementById("showMoreButton");
  var newTotalNumShown = totalNumShown + 10;

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

  //Gets the trades
  var xhr = new XMLHttpRequest();

  // Setup our listener to process completed requests
  xhr.onreadystatechange = function () {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
      if (xhr.status === OK) {
        var trades = JSON.parse(xhr.response);
        var tableBody = document.getElementById("transBody");
        var trade;
        var tradeNum = 0;
        for (tradeCode in trades) {
          tradeNum += 1;
          trade = trades[tradeCode];
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
        //Add increase the amount shown for next time
        if(tradeNum == 10) {
          button.setAttribute('onclick',"showMoreTrades('"+date + "'," + newTotalNumShown+")");
        } else {
          button.removeAttribute('onclick');
          button.innerHTML = "No More"
        }
      } else {
        alert('Error: ' + xhr.status); // An error occurred contentduring the request.
      }
    }
  };

  // Create and send a GET request
  // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
  // The second argument is the endpoint URL
  var URL = "http://localhost:5002/filterTrades/" + totalNumShown;

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
