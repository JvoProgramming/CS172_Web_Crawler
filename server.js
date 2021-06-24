const port = 8080;
var cors = require('cors')
const express = require('express');

const { Client } = require('@elastic/elasticsearch')
const client = new Client({
  cloud: {
    id: 'CS172_Final_Project:ZWFzdHVzMi5henVyZS5lbGFzdGljLWNsb3VkLmNvbTo5MjQzJDM4MGNmZjhhMDY2ZDQyOGQ5MTJhMmI5YTAzNjY4NTE0JDVlZGQ4YzAzNWQyNzQxNjhiMjRlNWI4ZjI2YzY4MDFm',
  },
  auth: {
    username: 'elastic',
    password: 'Vmt0Mnj5tuJL2fwAdpWSMvqi'
  }
})
var result; 
const app = express(); 
app.use(cors());

app.get("/findResult", async (request, response) => {
    var word = request.query.userInput; 
    //console.log(word);
    var query = {index: "index-0","body": {"query": {"match": {"html": word}}}}; 
    const { body } = await client.search(query);
    result = body.hits.hits;  
    response.send(result); 
}); 

app.listen(port, () => console.log(`Server listening on http://localhost:${port}`));
