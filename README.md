# email_service_python

I decided to create this specific script after various people told me to use legacy code to accomplish the intended.

That however "irked" me a bit so I just wrote my own - easy to understand - emailing script in python. 

The script essentially sends a configurable email to 3 - pre configured email addresses. It also attached 3 .csv files to the email. 

This script uses a json file to import the necessary server details to enable us to actually log in to send emails. See the config.json for more details on that.

I quickly ran the script in a virtual environment with the below dependencies. All working.

Just a note - there are file paths required for the script to actually work.
These file paths are simply the source folder where the actual code is located and the master folder - where the files we want to attach to the email is located.

# Dependancies:
Python 3.6

