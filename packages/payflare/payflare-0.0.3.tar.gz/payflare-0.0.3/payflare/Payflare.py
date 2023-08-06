import httpx
import hmac
from hashlib import sha256
import json
import time
import re

class Payments:
    def __init__(self, api_cli):
        self.__api = api_cli
    async def create(self, name: str, currency: str, amount: int, methods: list, expires_at: int = 0,
        description:str="", payer_email: str ="", redirect_after: str="", message_after:str=""):
        """Create a payment"""

        request_data = {
            "name": name,
            "currency": currency,
            "amount": amount,
            "methods": methods,
        }
        if expires_at != 0:
            request_data["expires_at"] = expires_at
        if description != "":
            request_data["description"] = description
        if payer_email != "":
            request_data["payer_email"] = payer_email
        if redirect_after != "":
            request_data["redirect_after"] = redirect_after
        if message_after != "":
            request_data["message_after"] = message_after
        resp = await self.__api.post("/payments", json=request_data)
        if resp.status_code != 200:
            raise Exception(resp.text)
        return {
            "ok": True,
            "id": resp.json()["id"],
            "checkout": f"https://payflare.io/pay/{resp.json()['id']}"
        }
class Webhooks:

    def construct_event(payload:str, signature:str, webhook_secret:str):
        """Construct a webhook event"""

        regex = r"^sig=(?P<sig>[0-9a-f]{64}),t=(?P<exp>[0-9]{10,14})$"
        matches = re.search(regex, signature)
        if matches is None:
            raise Exception("Invalid signature")
        signature_txt = matches.group("sig")
        exp = matches.group("exp")
        if (time.time() - int(exp)) > 60 * 3:
            raise Exception("Signature expired")
        if not hmac.compare_digest(signature_txt, hmac.new(webhook_secret.encode(), payload.encode(), sha256).hexdigest()):
            raise Exception("Invalid signature")
        return json.loads(payload)
class Payflare:
    def __init__(self, api_secret:str):
        self.__api = httpx.AsyncClient(base_url="https://api.payflare.com/",
            headers={"api-auth": f"Token {api_secret}", "Content-Type": "application/json"})
    @property
    def payments(self):
        return Payments(self.__api)
    @property
    def webhooks(self):
        return Webhooks()
    
    