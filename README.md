# Airtable API requests for Python <h1>**ATTENTION: this is only a test enviroment for learning purpose, not recommended for use**![project-logo](https://cdn-images-1.medium.com/max/800/1*ycLQdG3p7jCjOfgqnV5n_Q.gif)## What you can do:This script allow you to GET, POST, PATCH AND DELETE the rows on an Airtable data sheet.* You can launch command  from python terminal.* You can launch command from command line with CLI-airtable.* You can use test enviroment for debug purpose.## Requirements:* A config.YAML file on the installation path: _contents sample:_```base_key: 'your enviroments base code'table_name: 'your table name'api_key: 'your api key'```* pytest==5.3.0```pip install pytest==5.3.0```* PyYAML==5.2```pip install PyYAML==5.2```* requests==2.22.0```pip install requests==2.22.0```### Usage Example on python terminal:* **Read table contents:**```tbl.get()```will return exit code, id, name and code of items on table.* **Insert a new row:**```tbl.insert(**fields dictionary)```will return exit code, id, name and code of items on table.Dictionary must have the format: ```"Name"="item_name_to_add", "Code"="Item_related_code"```* **Edit rows:**```tbl.modify(target_row_id, **fields dictionary)```will return exit code, id, new name and code assigned to the target items.* **Delete rows:**```tbl.delete(target_row_id)```will return exit code, id, name and code of the items deleted.### Usage Example on Command Line:The function available on command line are the same abovementioned. ** Command line syntax is the following** ```python cli-airplay.py [-h] [-payload] [-target_id] table base apikey {ins,mod,del,get}```**Parameters description:**Parameters | Descrioption------------ | --------------h | Show program help-payload | A dictionary containing name and code. Used for insert or modify row purpose.-target_id | Represent the ID Number needed in case of row modification or deletion.table | The name of your tablebase | The base key of your work enviromentapikey | Your Airtable API key{ins,mod,del,get} | Choose the kind of request: insert, modify, delete, get.## Tanksgiving:An indeed thanks to my parents, my friend and to Alby for he's great patience and strong effort shown during this hard times.