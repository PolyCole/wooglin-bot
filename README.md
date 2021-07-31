<p>
  <img src="https://i.imgur.com/YR94laL.jpg" alt="Wooglin bot logo" width="800"></img>
</p>

![CircleCI](https://img.shields.io/circleci/build/github/WooglinAlphaZeta/wooglin-bot/main?style=for-the-badge)
<img alt="GitHub last commit" src="https://img.shields.io/github/last-commit/WooglinAlphaZeta/wooglin-bot?color=%20%23ff751a&style=for-the-badge">
<img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/WooglinAlphaZeta/wooglin-bot?style=for-the-badge">

### Introduction
This repository houses the code that facilitates user interaction in the BTP AZ Slack Workspace. The bot interacts with users, relying heavily on [wooglin-api](https://github.com/WooglinAlphaZeta/wooglin-api) for data collection and modifying, and [wooglin-nlu](https://github.com/WooglinAlphaZeta/wooglin-nlu) for Natural Language Understanding (NLU). The bot synthesizes the information provided by these two services and provides the user with straightforward interaction to accomplish the tasks necessary to run the chapter. 

### How It Works
The bot is written using Python, relying heavily on the Slack API. The bot also takes advantage of the Twilio API to facilitate chapter-wide communication via SMS. The bot itself is deployed using CircleCI and Serverless, where the bot eventually is released to the world as a series of AWS Lambda functions.
