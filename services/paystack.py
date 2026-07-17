import os
import requests

class PaystackService:
    def __init__(self):
        # Good practice: Pull your secret key from environment variables
        self.secret_key = os.environ.get("PAYSTACK_SECRET_KEY", "sk_test_your_secret_key_here")
        self.base_url = "https://api.paystack.co"
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def initialize_transaction(self, email: str, amount_in_naira: float, callback_url: str, metadata: dict = None):
        """
        Initializes a transaction on Paystack.
        Note: Paystack accepts amounts in KOBO (1 Naira = 100 Kobo).
        """
        url = f"{self.base_url}/transaction/initialize"
        
        # Convert Naira to Kobo
        amount_in_kobo = int(float(amount_in_naira) * 100)

        payload = {
            "email": email,
            "amount": amount_in_kobo,
            "callback_url": callback_url,
            "metadata": metadata or {}
        }

        try:
            response = requests.post(url, json=payload, headers=self.headers, timeout=10)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("status"):
                # Returns data dict containing authorization_url and reference
                return response_data.get("data")
            return None
        except requests.RequestException as e:
            print(f"Paystack Initialization Exception: {e}")
            return None

    def verify_transaction(self, reference: str):
        """
        Verifies a transaction using its reference string.
        """
        url = f"{self.base_url}/transaction/verify/{reference}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response_data = response.json()
            if response.status_code == 200 and response_data.get("status"):
                return response_data.get("data")
            return None
        except requests.RequestException as e:
            print(f"Paystack Verification Exception: {e}")
            return None