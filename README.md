# fetch-app #
Backend Intern Coding Challenge for Fetch Rewards

## Purpose: ##
This web service handles user points and transactions according to documentation found here (https://fetch-hiring.s3.us-east-1.amazonaws.com/points.pdf). The program objectives are
	- Add transactions for a specific payer and date
	- Spend points according to documentation rules
	- Return all payer point balances

## Requests: ##

Requests can be made to three different routes with following query params:

“/transaction”
	“payer”
	“points”
	“timestamp”

“/spend”
	“points”’

“/balance”
	no params

## Program usage: ##

The program utilizes the Flask framework and requires an environment with flask installed. Additionally, python-dotenv will need to be installed to ensure the .flaskenv file is correctly used to set environment variables. Both of these can be installed with pip:

pip install Flask python-dotenv

Once installed, the command “flask run” in the backend directory will start the server. (Necessary files are contained in a backend folder in the root directory to allow organized addition of front end components in the future)

To send requests, simply follow the routes and parameters outline above. Here are some sample requests:

JOE, 1000 points at 2020-11-01T14:00:00Z
http://<span></span>127.0.0.1:5000/transaction?payer=JOE&points=1000&timestamp=2020-11-01T14:00:00Z

Spend 500 points
http://<span></span>127.0.0.1:5000/spend?points=500

Check balance
http://<span></span>127.0.0.1:5000/balance

Requests can either be made directly on a browser or more systematically with an app like Postman.

(Note: Per documentation, no permanent data store is used, so any transactions made will be erased upon termination of the program)
