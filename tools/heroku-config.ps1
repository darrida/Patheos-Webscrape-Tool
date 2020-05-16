#!/bin/bash
#
# Purpose of script:
#  -Expidite setting heroku config each time
#
# Load module for generating random string
[Reflection.Assembly]::LoadWithPartialName("System.Web")
##############################################
heroku config:set FLASK_APP=flasky.py --app=webscrape-tool 
heroku addons:create heroku-postgresql:hobby-dev --app=webscrape-tool
heroku config:set FLASK_CONFIG=heroku --app=webscrape-tool 
$key = -join ((65..90) + (97..122) | Get-Random -Count 35 | % {[char]$_})
heroku config:set SECRET_KEY=$key --app=webscrape-tool
# sudo heroku config:set MAIL_USERNAME=bentestflask@gmail.com
# echo "Setup MAIL_PASSWORD separately"
# echo ""
echo "heroku config complete."
echo ""
##############################################
# Contact: darrida | darrida.py@gmail.com | tech.theogeek.com