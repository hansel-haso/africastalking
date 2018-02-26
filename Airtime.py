from schema import Schema, And, SchemaError
import json
from Service import APIService, AfricasTalkingException


def validate_amount(amount_str):
    try:
        parts = amount_str.split(' ')
        return len(parts[0]) == 3 and float(parts[1])
    except ValueError:
        return False


class AirtimeService(APIService):
    def __init__(self, username, api_key):
        super(AirtimeService, self).__init__(username, api_key)

    def _init_service(self):
        super(AirtimeService, self)._init_service()
        self._baseUrl = self._baseUrl + '/version1/airtime'

    def send(self, recipients, callback=None):

        try:
            schema = Schema([
                {
                    'phoneNumber': And(str, len),
                    'amount': And(str, lambda s: validate_amount(s))
                }
            ])
            recipients = schema.validate(recipients)
        except SchemaError:
            raise AfricasTalkingException('Invalid recipients')

        url = self._make_url('/send')
        params = {
            'username': self._username,
            'recipients': json.dumps(recipients)
        }
        return self._make_request(url, 'POST', headers=self._headers, params=params, callback=callback)
