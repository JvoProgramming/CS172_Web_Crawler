#!/bin/bash
# Username, Password, endpoint for elastic search
username=elastic; 
password=Vmt0Mnj5tuJL2fwAdpWSMvqi; 
servername=cs172-final-project-39758a.es.eastus2.azure.elastic-cloud.com:9243
# Index name
index=index-0; 
########### Delete the Index in case it exists ###########
echo "Delete index: $index" 
curl -X DELETE -u $username:$password "https://$servername/$index";
########### Post to Index ##########
# 1) Create index that ignores HTML characters when searching (note, it will still show HTML characters when retrieving result)
curl -X PUT -u $username:$password "https://$servername/$index?pretty" -H 'Content-Type: application/json' -d'{
  "settings": {
    "analysis": {
      "analyzer": {
        "htmlStripAnalyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase"],
          "char_filter": [ "html_strip" ]
        }
      }
    }
  },"mappings": {
      "properties": {
        "html": {
          "type": "text",
          "analyzer": "htmlStripAnalyzer"
        }
      }
  }
}'
# 5) Bulk load data. Create a json file that stores your data. 
curl -X POST -u $username:$password "https://$servername/$index/_bulk" -H "Content-Type: application/x-ndjson" --data-binary @data.json
########### Search from Index #########
echo "Running searchIndex"
echo "Options: "
select choice in Query_All Query_One_Word Exit
do 
case $choice in 
# Case 1
"Query_All")
echo $choice
curl -X GET -u $username:$password "https://$servername/$index/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match_all": { }
    }
}' > result.json;
;;
# Case 2
"Query_One_Word")
echo $choice; 
echo Enter the query word:
read query;
echo "You have entered: $query" 
curl -X GET -u $username:$password "https://$servername/$index/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "match": {
            "html": "'$query'"
        }
    }
}' > result.json;
;;
# Case 3
"Exit")
echo Exit
break
;;
*)
echo "Invalid Entry"
break
;;
esac 
done


