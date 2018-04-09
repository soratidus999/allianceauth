# Mediawiki

Media wiki is an open source Wiki

## Prepare your Settings

- Add `services.modules.mediawiki` to your `INSTALLED_APPS` list.
 - Append the following to your auth project's settings file:
 
    # Jabber Configuration
    MEDIAWIKI_URL = ''
    MEDIAWIKI_BOTUSER = ''
    MEDIAWIKI_BOTPASSWORD = ''


## Overview
https://www.mediawiki.org/wiki/MediaWiki

## Dependencies
None over base AA install, but always check https://www.mediawiki.org/wiki/Manual:Installation_guide

## Setup

https://www.mediawiki.org/wiki/Manual:Installation_guide

## AA Specific Config

Mediawiki by default is entirely open for user registration and page editing.

https://www.mediawiki.org/wiki/Manual:Preventing_access#Restrict_account_creation Provides a baseline config and an example of procedure

Apply the simple private wiki config

Log into the Wiki Admin, visit Special:BotPasswords

Create a bot user and password with the following rights

- Block and unblock users
- Create Accounts

Add the IP of your AA base install to the allowed list

the bot user will be created with the syntax username@botusername

This needs to be entered into the MEDIAWIKI_BOTUSER and MEDIAWIKI_BOTPASSWORD configs.

## Setup Complete
You may want to configure mediawiki past its default,