function deleteWarning(tradeID, notionalVal, predictedUpper, predictedLower) {
    // Set up our HTTP request
  var xhr = new XMLHttpRequest();

  // Setup our listener to process completed requests
  xhr.onreadystatechange = function () {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
      if (xhr.status === OK) {
        alert("Warning deleted"); // 'This is the returned text.'
        location.reload();
      } else {
        alert('Error: ' + xhr.status); // An error occurred during the request.
      }
    }
  };

  var URL = "http://localhost:5002/warningrules";
  var data = "tradeID=" + tradeID;
  data += "&notionalVal=" + notionalVal;
  data += "&predictedUpper=" + predictedUpper;
  data += "&predictedLower=" + predictedLower;

  if (confirm("Are you sure you want to delete this warning rule?")) {
      xhr.open('POST', URL, true);
      xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
      xhr.send(data);
    }
  }
