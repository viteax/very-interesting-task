# import json

import requests
import requests.auth

from config import Config, load_config

config: Config = load_config()

client_id = config.client_id
client_secret = config.client_secret

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post(
    "https://stepik.org/oauth2/token/",
    data={"grant_type": "client_credentials"},
    auth=auth,
)

token = response.json().get("access_token", None)
if not token:
    print("Unable to authorize with provided credentials")
    exit(1)

session = requests.session()
session.headers = {"Authorization": f"Bearer {token}"}

API_URL = "https://stepik.org/api"
# docs = session.get(f"{api_url}/docs/api-docs")
# print(json.dumps(docs.json(), indent=2))

# endpoint = "0"
# while endpoint:
#     endpoint = input()
#     temp = session.get(f"{api_url}{endpoint}")
#     print(json.dumps(temp.json(), indent=2))


# print("Return 0")
