## Kerala-Lottery-Scraper
![MIT License](https://img.shields.io/github/license/shine-jayakumar/Covid19-Exploratory-Analysis-With-SQL)

A web-scraper in Python to extract links to lottery results (pdf) from KeralaLottery.com. 

The script outputs the data in .csv format and sends an email to a default email address. It can also take an email address as a command-line argument.

The script runs in Headless Chrome mode enabling it to be deployed on Heroku and executed with Heroku CLI. 

![Scrapped Data To Email](https://github.com/shine-jayakumar/Kerala-Lottery-Scraper/blob/main/scapped.PNG)

**Table of Contents**

- [Packages](#Packages "Packages")
- [How To Deploy](#How-To-Deploy "How to Deploy")
- [Run The App](#Run-The-App "Run The App")
- [Getting Started With Heroku](#Getting-Started-With-Heroku "Getting Started With Heroku")
- [Script Link](#Script-Link "Script Link")


## Packages
- pandas
- selenium

  See the [Requirements.txt](https://github.com/shine-jayakumar/Kerala-Lottery-Scraper/blob/main/requirements.txt)


## How To Deploy
I hope you built your project in a virtual environment. It's going to be lot easier that way.

Make sure you [download and install Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) on your machine.

Create an account for yourself on Heroku.com

Steps:
1. Open Commmand Prompt/Shell and move to your project directory (ex: cd d:\projects\scraper)

1. Create a new repository in your project directory
     ```
        git init 
     ```
     
1. Add everything in the directory to the repository
     ```
        git add . 
     ```
1. Commit
     ```
        git commit -am "Initial Commit" 
     ```
1. Login to Heroku from the command prompt
     ```
        heroku login
     ```
   A new browser instance will open up automatically, allowing you to login.
   Click on the login button and wait for the confirmation, after which you can close the tab and return to the command prompt.
   
1. Creating a new app
     ```
        heroku create
     ```
1. Push the git
     ```
        git push heroku master
     ```
Your app is now successfully deployed.


## Run The App

   ```
      heroku run python scraper.py
   ```
   
## Getting Started With Heroku

Take a look at this quick guide to [Getting Started on Heroku with Python](https://devcenter.heroku.com/articles/getting-started-with-python)


## Script Link
**Link:** [scraper.py](https://github.com/shine-jayakumar/Kerala-Lottery-Scraper/blob/main/scraper.py)

Disclaimer: ***This script and information provided in this project is for educational purposes only***
