import os

from firebase.functions.lib.adax.adax_client import AdaxClient

if __name__ == '__main__':
    credentials = os.environ.get('ADAX_API_CREDENTIALS')
    if (credentials is None):
        print("Please set ADAX_API_CREDENTIALS environment variable")
        exit(1)
    account_id = os.environ.get('ADAX_ACCOUNT_ID')
    if (account_id is None):
        print("Please set ADAX_ACCOUNT_ID environment variable")
        exit(1)
    
    client = AdaxClient(credentials, account_id)
    token = client.get_token()
    client.get_homes_info(token)

