# Python based Auto Email Job (email_service_python)

#Aim:

I decided to create this specific script after various people told me to use legacy code to accomplish the intended.

That however "irked" me a bit so I just wrote my own - easy to understand - emailing script in python. 

# Basics:

The script essentially sends a configurable email to 3 - pre configured email addresses. It also attached 3 .csv files to the email. 

# Json Object (configuration file):

This script uses a json object, (because json is awesome) to import the necessary server details to enable us to actually log in to send emails. 

See the config.json for the specifics

Only the json object needs to be edited for the script to work. Remember Python 3.6.

# File paths:

Various predetermined file paths are required for the script to actually work.
1. Source directory.
2. Storage directory. (where the files we want to attach to the email is located)

# Dependancies:
Python 3.6

# Logging:
There isnt any logging in this project. It may be a good idea to add it to the project somewhere in the future.

