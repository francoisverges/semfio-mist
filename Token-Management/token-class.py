import os
import json
import requests


class Token:

    """Mist Token Object"""

    def __init__(self):
        """
            Initialized the Mist Token object.

            Set the MASTER_TOKEN variable:
                - Retrieve the environment variable called MIST_TOKEN
                - Make sure the this environ is set on your system
                    - Run this command on MacOS: export MIST_TOKEN='<your-token-here>'
        """
        self.MASTER_TOKEN = os.environ['MIST_TOKEN']

    def get_tmp_token(self):
        """
            Creates a Mist token 'on the fly' to be used witin a specific script.

            The following API call is made to the Mist Cloud to create a new token:
                POST https://api.mist.com/api/v1/self/apitokens

            Set the following class variables:
             - tmp_token_key: temporary token KEY received from Mist Cloud after creation
             - tmp_token_id: temporary token ID received from Mist Cloud after creation
        """
        api_url = "https://api.mist.com/api/v1/self/apitokens"
        headers = {"Content-Type": "application/json",
                   "Authorization": f"Token {self.MASTER_TOKEN}"}
        try:
            response = requests.post(api_url, data={}, headers=headers)
            if response.status_code == 200:
                token = json.loads(response.text)
                self.tmp_token_key = token['key']
                self.tmp_token_id = token['id']
                print(f"Temporary Token created: {self.tmp_token_key}\nID: {self.tmp_token_id}")
            else:
                raise ValueError(
                    f"Error connecting to Mist API!\tRESPONSE:'{response.status_code} - {response.text}'")
        except Exception:
            raise

    def delete_tmp_token(self):
        """
            Deletes the temporary Mist Token stored in self.tmp_token_key
            using its ID stored in self.tmp_token_id

            The following API call is made to the Mist Cloud to delete the token:
                DELETE https://api.mist.com/api/v1/self/apitokens/:token_id
        """
        if "tmp_token_id" in self.__dict__:
            api_url = f"https://api.mist.com/api/v1/self/apitokens/{self.tmp_token_id}"
            headers = {"Content-Type": "application/json",
                       "Authorization": f"Token {self.MASTER_TOKEN}"}
            try:
                response = requests.delete(api_url, headers=headers)
                if response.status_code == 200:
                    print(f"Token deleted\nID: {self.tmp_token_id}")
                else:
                    raise ValueError(
                        f"Error connecting to Mist API!\tRESPONSE:'{response.status_code} - {response.text}'")
            except Exception:
                raise
        else:
            raise ValueError(f"tmp_token_id does not exits.")


# Tests
# token = Token()
# token.get_tmp_token()
# print("--> We would be running our large script here making our API calls using the tmp token.")
# token.delete_tmp_token()
