import requests
import base64
import datetime
from django.conf import settings

def get_mpesa_access_token():
    """
    Fetches a valid MPESA access token.
    Ensure you have set MPESA_CONSUMER_KEY and MPESA_CONSUMER_SECRET in settings.py.
    """
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    response = requests.get(api_url, auth=(consumer_key, consumer_secret))
    response_data = response.json()

    return response_data.get("access_token", None)

def lipa_na_mpesa(phone_number, amount):
    """
    Initiates an STK Push request.
    """
    access_token = get_mpesa_access_token()  # Fetch MPESA token
    if not access_token:
        return {"error": "Failed to obtain MPESA access token"}

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    business_short_code = "174379"  # Default sandbox Paybill
    passkey = settings.MPESA_PASSKEY
    password = base64.b64encode(f"{business_short_code}{passkey}{timestamp}".encode()).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "BusinessShortCode": "2547XXXXXXXX",  # Your own MPESA phone number
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",  # MPESA still requires this
        "Amount": amount,
        "PartyA": phone_number,  # Customer's phone number
        "PartyB": "254110928039",  # Your own MPESA phone number
        "PhoneNumber": phone_number,  # Customer's phone number
        "CallBackURL": "https://5efc-41-80-113-54.ngrok-free.app/mpesa/callback/",
        "AccountReference": "Personal MPESA Payment",
        "TransactionDesc": "Payment to personal MPESA",
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
