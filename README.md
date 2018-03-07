
 # What is Indexer?

Articles in the files in the Dataset directory were taken from Reuters.

Indexer module crawls on those articles and creates a dictionary and inverted index map.

Querry processor module executes batch queries and shows document ids that matches the queries.


 # How to Run Indexer? 

 ## Step 1

Run indexer python script to create two files named dictionary.txt and

 inverted-index.txt. Former contains words-id mapping, and 

 latter contains inverted index map for each word id.

 ```
 >python3 indexer.py
 
 ```

 ## Step 2

  Run query_matcher.py script with a string argument of file name on the 

  command line. As a result, you will see a file that contains query results 

  to queries in the argument file. Queries should be given line by line and 
 
  results of the queries will be given line by line as well.

  ```
 >python3 query_matcher.py <"your_query_file_diretory">
 
 ```
