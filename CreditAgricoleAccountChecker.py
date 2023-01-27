import json
import urllib3
import requests
from termcolor import colored


refresh_token = 'VOTRE_REFRESH_TOKEN' # Obtenable en utilisant un proxy MItM
hashid = 'VOTRE_HASHID' # Obtenable en utilisant un proxy MItM

# Disable insecure request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_tokens():
    headers = {
        'Content-Type': 'application/json',
        'Correlationid': '0',
        'Hashid': '' + hashid + '',
        'Connection': 'close',
    }

    json_data = {'refresh_token': '' + refresh_token + ''}

    response = requests.post(
        'https://nmb.credit-agricole.fr/authentication/v1/refresh_token',
        headers=headers,
        json=json_data,
        verify=False,
    )

    return response.json()['access_token'], response.json()['refresh_token']


def get_account_details(access_token):
    headers = {
        'Content-Type': 'application/json',
        'Correlationid': '0',
        'Authorization': 'Bearer ' + access_token + '',
        'Hashid': '' + hashid + '',
        'Connection': 'close',
    }

    response = requests.get('https://nmb.credit-agricole.fr/home/v1/first_account', headers=headers, verify=False)
    
    return response.json()


# Getting access and refresh tokens
tokens = get_tokens()

access_token = tokens[0]
refresh_token = tokens[1]

# Getting account details
account_details = get_account_details(access_token)

# Getting account balance
account_name = account_details['account']['label']
contract_number = account_details['account']['contract_number']

account_balance = account_details['account']['balance']['amount']
balance_currency = account_details['account']['balance']['currency']

print(account_name + ' : ' + contract_number)
print(str(account_balance) + ' ' + balance_currency)