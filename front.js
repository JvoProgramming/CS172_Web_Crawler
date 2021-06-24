

function findResults()
{
  var outputData = document.getElementById("results");
  outputData.innerHTML = "";
  let params = "userInput=" + document.getElementById("searchBox").value; 
  var xhttp = new XMLHttpRequest(); 
  xhttp.responseType = 'json';
  xhttp.open("GET", "http://localhost:8080/findResult?" + params, true);
    xhttp.onload = function() {
      var jsonResponse = xhttp.response; 
      console.log("JSONResponse: " + jsonResponse);
      let hits = jsonResponse;
      console.log(hits);
      if(hits.length == 0){
        outputData.innerHTML = "No Results";
      }
      else{
        for(let i = 0; i < hits.length; i++){
          let title = hits[i]._source.html.match(/\(([^)]+)\)/)[1];
          let docText = hits[i]._source.html.replace(/\(([^)]+)\)/, "");
          let link = docText.split(" ")[1];
          let text = docText.slice(link.length+1,820) + "..."
          console.log(link)
          //let link = hits[i]._source.html
          outputData.innerHTML += "<li>" +
                                    "<div>" + 
                                      "<a" + " href=\"" + link + "\" + " + ">" + title + "</a>" +   
                                      "<p>" + "Score: " + hits[i]._score + "</p>" + 
                                      "<p>" + text + "</p>" +
                                    "</div>" +
                                  "</li>";
        }
      }
  }
  xhttp.send(null); 
  //console.log('front.js being called');

}


