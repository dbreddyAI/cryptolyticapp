# Flask App Documentation
Flask app allows user to request crypto prediction data and it's deployed on AWS Elastic Beanstalk.

[Current Deployment Link](http://cryptolytic-env.niu7nzrmmi.us-east-1.elasticbeanstalk.com)

# Table of Contents
1. [Flask App Endpoints](#endpoints)
2. [Deployment on AWS EB](#EB Deployment)



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
