# Flask App Documentation
Flask app allows user to request crypto prediction data and it's deployed on AWS Elastic Beanstalk.

[Current Deployment Link](http://cryptolytic-env.niu7nzrmmi.us-east-1.elasticbeanstalk.com)
Work in progress

[API Documentation](http://cryptolytic-env.niu7nzrmmi.us-east-1.elasticbeanstalk.com/api)


# Table of Contents
1. [Quick Rundown](#sum)
2. [Flask App Endpoints](#endpoints)
3. [Deployment on AWS EB](#EB Deployment)
4. [Built With](#dependency)
5. [What's Next](#next)

## Quick Rundown  <a name="sum"></a>
This flask application provides trading predictions and arbitrage prediction. More LATER :)

## Flask App Endpoints <a name="endpoints"></a>

### Homepage - [/]
A `homepage` render template
 
### API Documentation - [/api]
A `api` doc render template page

### Display Trade Predictions - [/display_tr]
A `DF Table` of trade predictions render template

### Display Arbitrage Predictions - [/display_arb]
A `DF Table` render template

### Trade Prediction - [/trade_rec]
Returns this endpoint if user requested trade predictions

Method: ["GET", "POST"]

### Arbitrage Prediction - [/arb]
Returns this endpoint if user requested arbitrage predictions

Method: ["GET", "POST"]

### Trade API - [/trade]
Returns a json result of all available trade predictions

Method: ["GET"]

Rate Limit: 10 per minute by IP Address

 Returns: ``` {"results":
"{('exchange', 'trading_pair'): [{
'p_time': 'time',
‘period’: ‘minutes’,
'prediction': 'result'}], }"} ```
  
### Arbitrage API - [/arbitrage]
Returns a json result of all available arbitrage predictions

Method: ["GET"]

Rate Limit: 60 per minute by IP Address

Returns: ``` {"results":"{
('exchange_1', 'exchange_2', 'trading_pair'): [
{'p_time': 'time',
'prediction': 'result'}
]} ```

## Deployment Instruction for AWS Elastic Beanstalk <a name="EB Deployment"></a>
Follow this guide for now [Medium Article](https://medium.com/analytics-vidhya/deploying-a-flask-app-to-aws-elastic-beanstalk-f320033fda3c)

## Built With <a name="dependency"></a>
* [flask](https://pypi.org/project/Flask/) - Application Framework
* [psycopg2](https://pypi.org/project/psycopg2/) - PostgresSQL database adapter
* [Amazon RDS](https://aws.amazon.com/rds/?nc2=h_ql_prod_fs_rds) - Flask queries a RDS DB

## What's Next <a name="next"></a>
* Change trade recommender to only predict crypto currency price movement without exchange input
* Add more exchanges and trading pair options for arbitrage predictions
* Track top currency price change and display it with the predictions
* Notification system 
* Configure Flask endpoint for a trading bot and give instructions
