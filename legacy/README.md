<p>
  <img src="https://i.imgur.com/YR94laL.jpg" alt="Wooglin bot logo" width="800"></img>
</p>

***
### Table of Contents

* [Introduction](#Introduction)
* [Documentation](#Documentation)
* [Technicals](#Technicals)
***
### Introduction
Woolgin Bot is the code powering the Wooglin Slack Bot that lives in the Slack workspace of the Alpha Zeta chapter of Beta Theta Pi. Wooglin helps to manage mass communication through SMS, Chapter attendance and standing tracking, and specified SMS communications as necessary, by utilizing a stand-alone api, Wooglin API. 

***
### Documentation
The following outlines the go-to phrasing that the bot has been trained on excessively. Using this phrasing increases the probability that the bot understands what you want.

| Goal          | Phrasing           |
| :------------ | ------------- |
| Sending a text to someone     | Wooglin, send a text message to [person] saying "[message]" |
| Sending the sober bro information to someone | Wooglin, please send [person] the sober bro information for [time] |
| Sending a message to the executive board | Wooglin, please send the executive board a text message saying [message] | 
| Getting stored info on someone     | Wooglin, please get all information on [person].      |
| Getting unexcused absences | Wooglin, how many times has [person] been unexcused from chapter?      |
| Getting excused absences | Wooglin, how many times has [person] been excused from chapter? |
| Getting excuses for missing chapter | Wooglin, what have been [person]'s excuses for missing chapter? |
| Getting phone number | Wooglin, what is [name]'s phone number? |
| Getting roll number | Wooglin, what is [name]'s roll number? |
| Getting sober bros | Wooglin, who are the sober bros on [date] | 
| Adding someone as a sober bro | Wooglin, [name] is a sober bro on [date] | 
| Removing someone as a sober bro | Wooglin, [name] is not a sober bro on [date] |

***
### Technicals
Update needed. Wooglin physically is a series of python scripts zipped up and stored in an S3 bucket. The script triggers when Wooglin's API sends a POST request to AWS Lambda. The bot uses AWS DynamoDB for storage. To send text messages, Wooglin uses the Twilio SMS API. For general Natural Language Processing, Wooglin uses Wit.ai's NLP engine. 
