from dataclasses import dataclass
import os
import requests
import json


@dataclass()
class Airtable:
    base_id: str
    api_key: str
    table_name: str

    def create_records(self, data={}):
        if len(data.keys()) is 0:
            return False
        endpoint = f"https://api.airtable.com/v0/{self.base_id}/{self.table_name}"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "records": [
                {
                    "fields": data,
                }

            ]
        }

        r = requests.post(endpoint, json=data, headers=headers)
        return r.status_code == 200 or r.status_code == 201

    def retrieve_record(self, wallet_address):
        if wallet_address is None:
            return False

        if len(wallet_address) < 42:
            return False

        # https://api.airtable.com/v0/appygGt0rRgfh6qxA/fastapi-to-airtable?fields%5B%5D=Notes&filterByFormula=SEARCH(%22ux%22%2C+Notes)&api_key=keyJwQSSqAZnD8KYR
        endpoint = f'https://api.airtable.com/v0/{self.base_id}/{self.table_name}?fields%5B%5D=wallet_address&filterByFormula=SEARCH("{wallet_address}"%2C+wallet_address)&api_key={self.api_key}'

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        r = requests.get(endpoint)
        # convert data to nested dictionary structure
        data = json.loads(r.text)
        records = data.get('records')
        print(records)
        if (records):
            id = records[0]['id']  # retrieve record
            endpoint = f'https://api.airtable.com/v0/{self.base_id}/{self.table_name}/{id}'
            r = requests.get(endpoint, headers=headers)
            data = json.loads(r.text)
            fields = data.get('fields')
            print(fields)
            # check to see if whitelist index exists, if not, user is not whitelisted
            try:
                whitelist = fields['whitelist']
            except KeyError:
                return False

            return True
        # wallet doesnt exist in table
        else:
            return False
