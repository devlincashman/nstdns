import time
import os
import json
import requests

DOMAIN = os.environ.get("DOMAIN")
NAME = os.environ.get("NAME")
KEY = os.environ.get("KEY")
SECRET = os.environ.get("SECRET")

TYPE = os.environ.get("TYPE", "A")
TTL = os.environ.get("TTL", "600")
FREQUENCY = os.environ.get("FREQUENCY", "15")

godaddy_headers = {
    "Authorization": f"sso-key {KEY}:{SECRET}",
    "Content-Type": "application/json",
    "accept": "application/json",
}

while True:
    godaddy_ip = requests.get(
        f"https://api.godaddy.com/v1/domains/{DOMAIN}/records/{TYPE}/{NAME}",
        headers=godaddy_headers,
    ).json()[0]["data"]

    home_ip = requests.get("http://ipinfo.io/json").json()["ip"]

    if godaddy_ip != home_ip:
        print(
            f"Home IP of {home_ip} is different than GoDaddy DNS IP of {godaddy_ip}, updating now!",
            flush=True,
        )

        update_dns_ip_json = [
            {
                "data": home_ip,
                "ttl": int(TTL),
            }
        ]

        godaddy_ip_update = requests.put(
            f"https://api.godaddy.com/v1/domains/{DOMAIN}/records/{TYPE}/{NAME}",
            headers=godaddy_headers,
            data=json.dumps(update_dns_ip_json),
        )

    if godaddy_ip == home_ip:
        print(
            f"Home IP of {home_ip} is the same as GoDaddy DNS IP of {godaddy_ip}.",
            flush=True,
        )
    time.sleep(int(FREQUENCY) * 60)
