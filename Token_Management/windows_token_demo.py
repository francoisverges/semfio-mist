""" 

This script that demonsrates how to use token_class.py on Windows

Before running the script, you must define a user-level environmental
variable that contains your Mist API token. This will be used to access 
the Mist cloud and create the required temporary key(s) to perfom
scripted actions.

The token_class module relies on the presence of an environmental 
variable called MIST_TOKEN to authorize access to the Mist API. This
env var must contain the value of a valid token that has been 
previousy created via the Mist API, e.g. using POSTMAN or some other
API access tool - see the following URL for an example:

    https://www.mist.com/documentation/using-postman/).

To create the user env var, use the following command from a 
command window on a Windows 10 machine:

    setx MIST_TOKEN "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

To verify the env var has been correctly created, open a new command
windows and type the following command to verify that the env var
is now gloablly available to the user account being used:

    echo %MIST_TOKEN%

Note that the env var is only available in a NEW command window. The env 
var is now permanently avaialble to all processes running under the current
user account. The env var will not be available to other users on the same
machine.

To remove the env var value, set the env var with a blank value in a command
window (the env var will still exist, but will have no value):

    setx MIST_TOKEN ""

Or, alternatively it may be deleted via the Windows 10 GUI environmental 
variable editing tool: Start > Control Panel > System & Security >
System > Advanced System Settings > Environmental Variables (User section)

""" 
from token_class import Token

# create Token obj
master_token_obj = Token()

# get a temporary token so that we can do some stuff
temp_mist_token = master_token_obj.get_tmp_token()

# do some stuff here (e.g. list WLANs)
# TBA

# clean up by removing our temporary token
master_token_obj.delete_tmp_token()
