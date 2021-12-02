function addTrade() {
  //Gets all the data from the form
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

  // Validate the form data

  var validData = true;
  if (!validateDate(datePlaced)) {
    validData = false;
    var input1 = document.getElementById("datePlace");
    input1.style.borderColor = "red";
    input1.onclick = function(){input1.removeAttribute("style")};
  }

  if (!validateDate(dateMature)) {
    validData = false;
    var input2 = document.getElementById("maturityDate");
    input2.style.borderColor = "red";
    input2.onclick = function(){input2.removeAttribute("style")};
  }

  if (!validateProduct(product)) {
    validData = false;
    var input3 = document.getElementById("product");
    input3.style.borderColor = "red";
    input3.onclick = function(){input3.removeAttribute("style")};
  }

  if (!validateQuantity(quantity)) {
    validData = false;
    var input4 = document.getElementById("quantity");
    input4.style.borderColor = "red";
    input4.onclick = function(){input4.removeAttribute("style")};
  }

  if (!validateParties(buying, selling)) {
    validData = false;
    var input5 = document.getElementById("buyingParty");
    input5.style.borderColor = "red";
    input5.onclick = function(){input5.removeAttribute("style")};
    var input6 = document.getElementById("sellingParty");
    input6.style.borderColor = "red";
    input6.onclick = function(){input6.removeAttribute("style")};
  }

  if (!validateCurrency(notionalCurr)) {
    validData = false;
    var input7 = document.getElementById("currenyNotional");
    input7.style.borderColor = "red";
    input7.onclick = function(){input7.removeAttribute("style")};
  }

  if (!validatePrice(notionalPrice)) {
    validData = false;
    var input8 = document.getElementById("priceNotional");
    input8.style.borderColor = "red";
    input8.onclick = function(){input8.removeAttribute("style")};
  }

  if (!validateCurrency(underCurr)) {
    validData = false;
    var input9 = document.getElementById("currenyUnder");
    input9.style.borderColor = "red";
    input9.onclick = function(){input9.removeAttribute("style")};
  }

  if(!validatePrice(underPrice)) {
    validData = false;
    var input10 = document.getElementById("priceUnder");
    input10.style.borderColor = "red";
    input10.onclick = function(){input10.removeAttribute("style")};
  }

  if(!validatePrice(strikePrice)) {
    validData = false;
    var input11 = document.getElementById("strikePrice");
    input11.style.borderColor = "red";
    input11.onclick = function(){input11.removeAttribute("style")};
  }

  if(!validateProduct(product)) {
    validData = false;
    var input12 = document.getElementById("product");
    input12.style.borderColor = "red";
    input12.onclick = function(){input12.removeAttribute("style")};
  }

  // Set up our HTTP request
var xhr = new XMLHttpRequest();

// Setup our listener to process completed requests
xhr.onreadystatechange = function () {
  var DONE = 4; // readyState 4 means the request is done.
  var OK = 200; // status 200 is a successful return.
  if (xhr.readyState === DONE) {
    if (xhr.status === OK) {
      var response = JSON.parse(xhr.response);
      if (response["result"] == 'Trade successfully entered.') {
        if (response["warning"].hasOwnProperty('tradeID')) {
          alert("Trade added however, notional value of "+response["warning"]["notionalVal"]+ " is not between " + response["warning"]["predictedLower"] + " and "+response["warning"]["predictedUpper"]);
        } else {
          alert(response["result"]);
        }
        location.href = "http://localhost/add";
      } else {
        alert(response["result"]);
      }
    } else {
      alert('Error: ' + xhr.status); // An error occurred during the request.
    }
  }
};

// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
var URL = "http://localhost:5002/addTrade";
var data = "tradeID=null";
data += "&product=" + product;
data += "&buyingParty=" + buying;
data += "&sellingParty=" + selling;
data += "&notionalPrice=" + notionalPrice;
data += "&notionalCurrency=" + notionalCurr;
data += "&quantity=" + quantity;
data += "&datePlaced=" + datePlaced;
data += "&maturityDate=" + dateMature;
data += "&underlyingPrice=" + underPrice;
data += "&underlyingCurrency=" + underCurr;
data += "&strikePrice=" + strikePrice;

if (validData) {
  if (confirm("Are you sure the information is correct?")) {
    xhr.open('POST', URL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

    xhr.send(data);
    }
  }
}
