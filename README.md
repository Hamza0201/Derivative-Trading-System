# Derivative-Trading-System
CS261 Group Project - Group 26

## Linux Instructions
### Back-end Webserver
You will need Flask to run this which requires pip to install. These are the ubuntu commands:

`sudo apt install python-pip3`

`pip3 install flask flask-jsonpify flask-sqlalchemy flask-restful`

`pip install mysql-connector`

`pip3 install sklearn`

Then you can run it with:
`python3 api.py`

If it is the first time running it then you will need to run:
`python database.py`

Then go to
[www.localhost:5002/](`www.localhost:5002/`)

*Note: this server is not secure and should not be exposed to the internet*

### Front-end Webserver
Copy the front-end files into the apache webserver of your choice.

Mostly tested on XAMP but which one you use does not actually matter just need to support PHP and cURL and is useful if it has a MySQL database support

*Note: this server is not secure and should not be exposed to the internet*

### MYSQL Database
XAMP or other APACHE webservers have a MYSQL server built into them.
Just create a database with the name bankDB

Then change the default password of root to password123

run `python database.py` to build the database
