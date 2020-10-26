// Kelly Buchanan
// kbuchana
// Timothy Gallagher
// tgallag6

send = document.getElementById("send-button");
console.log("IN FILE");
// button event function
send.onmouseup = makeServerRequest;

clear = document.getElementById("clear-button");
clear.onmouseup = clearMessage;

function makeServerRequest() {
  var URL = "http://student10.cse.nd.edu:51091/movies/57";
  console.log('url: ', URL)
  /****** GET INFO FROM FORM *******/

  // from dropdown menu
  var serv = document.getElementById('select-server-address').selectedIndex;
  var url = document.getElementById('select-server-address').options[serv].value;
  var port = document.getElementById('input-port-number').value;

  // parse by request with GET as default
  var req = "GET";
  if (document.getElementById('radio-get').checked) {
    req = "GET";
  } else if (document.getElementById('radio-put').checked) {
    req = "PUT";
  } else if (document.getElementById('radio-post').checked) {
    req = "POST";
  } else if (document.getElementById('radio-delete').checked) {
    req = "DELETE";
  }

  // set key from form
  var key = null;
  if (document.getElementById('checkbox-use-key').checked) {
    key = document.getElementById('input-key').value;

  }

  // get total url
  var newUrl = url + ":" + port + "/movies/";
  if (key != null) {
    newUrl = newUrl + key;
  }

  // get body of message
  var body = null;
  if (document.getElementById('checkbox-use-message').checked) {
    body = document.getElementById('text-message-body').value;
  }

  // concat the values
  var values = [req, newUrl, body];
  console.log("VALS: ", values)

  /****** MAKE REQUEST TO SERVER *******/

  // open http request
  var xhr = new XMLHttpRequest();
  xhr.open(values[0], values[1], true);

  // on event get movie
  xhr.onload = function(evnt) {
    if (xhr.readyState === 4) {
      document.getElementById('response-label').innerHTML = xhr.responseText;
      var movie = JSON.parse(xhr.responseText);
      var title = movie['title'];
      var genres = movie['genres'];
      document.getElementById('answer-label').innerHTML = title + " belongs to the genres: " + genres;
    } else {
      //  error check
      console.error(xhr.statusText);
    }
  };

  xhr.onerror = function(evnt) {
    // error check
    console.error(xhr.statusText);
  }

  xhr.send(values[2]);
}

function clearMessage() {
  console.log("CLEAR")
  location.reload()
}
