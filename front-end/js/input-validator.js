function validatePrice(price) {
  if (isNaN(price) || price == "") {
    return false;
  }
  if (price < 0) {
    return false;
  }
  return true;
}

function validateQuantity(quantity) {
  if (isNaN(quantity) || quantity == "") {
    return false;
  }
  if (quantity < 0) {
    return false;
  }
  return true;
}

function validateParties(buying, selling) {
  if (buying != selling && validateParty(buying) && validateParty(selling)) {
    return true;
  }
  return false;
}

function validateParty(party) {
  if (party == "") {
    return false;
  }
  return true;
}

function validateCurrency(currency) {
  if (currency == "") {
    return false;
  }
  return true;
}

function validateDate(date) {
  var parsedDate = Date.parse(date);
  return (isNaN(date) && !isNaN(parsedDate));
}

function validateProduct(product) {
  if (product == "") {
    return false;
  }
  return true;
}

function validateTradeID(tradeID) {
  if (tradeID == "") {
    return false;
  }
  return true;
}
