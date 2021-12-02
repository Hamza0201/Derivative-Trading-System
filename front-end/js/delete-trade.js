function deleteTrade() {
  //Gets all the data from the form
  var tradeID = document.getElementById("tradeID").value;

  // TODO: use AJAX to make an API request.
  var xhr = new XMLHttpRequest();

  // Setup our listener to process completed requests
  xhr.onreadystatechange = function () {
    var DONE = 4; // readyState 4 means the request is done.
    var OK = 200; // status 200 is a successful return.
    if (xhr.readyState === DONE) {
      if (xhr.status === OK || xhr.status === 0) {
        alert(xhr.responseText); // 'This is the returned text.'
        window.location.replace("http://localhost/alter");
      } else {
        alert('Error: ' + xhr.status); // An error occurred during the request.
      }
    }
  };

  // Create and send a GET request
  // The first argument is the post type (GET, POST, PUT, DELETE, etc.)
  // The second argument is the endpoint URL
  var URL = "http://localhost:5002/deleteTrade";
  var data = "tradeID=" + tradeID;

  if (confirm("Are you sure you want to delete this trade?")) {
    xhr.open('POST', URL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send(data);
  }
}
