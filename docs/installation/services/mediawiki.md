# Mediawiki

Add `services.modules.mediawiki` to your `INSTALLED_APPS` list and run migrations before continuing with this guide to ensure the service is installed.

## Overview
https://www.mediawiki.org/wiki/MediaWiki

## Dependencies
None over base AA install, but always check https://www.mediawiki.org/wiki/Manual:Installation_guide

## Setup

https://www.mediawiki.org/wiki/Manual:Installation_guide

## AA Specific Config

Mediawiki by default is entirely open for user registration and page editing.

https://www.mediawiki.org/wiki/Manual:Preventing_access#Restrict_account_creation Provides a baseline config and an example of procedure

Apply the simple private wiki config and move on to allowing AA to have access

logged in as the wiki admin, visit Special:BotPasswords

create a bot user and password with the following rights

Block and unblock users
Create Accounts

And add the IP of your AA base install to the allowed list

the bot user will be created with the syntax username@botusername

punch this and your password into settings.py in the appropriate location

## Setup Complete
You may want to configure mediawiki past its default, as standard its very barebones.

Hopefully i get to some example skins, extensions etc.