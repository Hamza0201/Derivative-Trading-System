function changeMode() {
  // TODO: use AJAX to make an API request.

  // Set up our HTTP request
var xhr = new XMLHttpRequest();

// Setup our listener to process completed requests
xhr.onreadystatechange = function () {
  var DONE = 4; // readyState 4 means the request is done.
  var OK = 200; // status 200 is a successful return.
  if (xhr.readyState === DONE) {
    if (xhr.status === OK) {
      alert("Training Mode Changed"); // 'This is the returned text.'
      location.reload();
    } else {
      alert('Error: ' + xhr.status); // An error occurred during the request.
    }
  }
};

// Create and send a GET request
// The first argument is the post type (GET, POST, PUT, DELETE, etc.)
// The second argument is the endpoint URL
var URL = "http://localhost:5002/trainingMode";

if (confirm("Are you sure you want to train?")) {
    xhr.open('POST', URL, true);

    xhr.send(null);
  }
}
