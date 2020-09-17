import base64
from datetime import datetime
import json

from django.http import HttpResponse
from django.urls import reverse
import requests

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth

CONSUMER_KEY = 'wY6MrrA7TKS7TCuSWRDvuIBu7Snlj4b4'
CUSTOMER_SECRET = 'lCHOsZMh4ofQ6Ew3'
Business_short_code = "174379"
API_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
mpesa_passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

# todo implement text back

def get_token():
    r = requests.get(API_URL,
                     auth=HTTPBasicAuth(CONSUMER_KEY, CUSTOMER_SECRET))
    mpesa_access_token = json.loads(r.text)
    return mpesa_access_token['access_token']


def get_password():
    time = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = Business_short_code + mpesa_passkey + time

    online_password = base64.b64encode(data_to_encode.encode())

    decode_password = online_password.decode('utf-8')
    return decode_password, time


def getAccessToken(request):
    consumer_key = 'wY6MrrA7TKS7TCuSWRDvuIBu7Snlj4b4'
    consumer_secret = 'lCHOsZMh4ofQ6Ew3'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)


@method_decorator(csrf_exempt, name="dispatch")
class Lipa_na_mpesa_online(View):
    def get(self, request):
        pass

    def post(self, request):
        """ Make payment for an event by picking the events price and the users phone number to trigger payment """
        # TODO
        """ ====================To do allow user to pay by specifying phonenumber, for the users who are not logged in================= """
        SUCCESS = 25

        current_request = request
        amount = 1
        phonenumber = request.POST.get('phone_number')
        access_token = get_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        password, time = get_password()
        request = {
            "BusinessShortCode": Business_short_code,
            "Password": password,
            "Timestamp": time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phonenumber,
            "PartyB": Business_short_code,
            "PhoneNumber": phonenumber,  # replace with your phone number to get stk push
            "CallBackURL": f"http://{request.get_host()}{reverse('call_back')}",
            "AccountReference": f'Payment to Buxs',
            "TransactionDesc": f"Pay for items"
        }

        response = requests.post(api_url, json=request, headers=headers)
        response_json = json.loads(response.text)
        print(response_json)

        # error example
        # {'requestId': '15580-24058973-1', 'errorCode': '400.002.02', 'errorMessage': 'Bad Request - Invalid CallBackURL'}
        try:
            response_code = int(response_json['ResponseCode'])
        except KeyError:
            return HttpResponse(f'Failed to connect to safcom error -> {response_json}')
        if response_code == 0:
            # merchant_r_id = response_json['MerchantRequestID']
            # checkout_r_id = response_json['CheckoutRequestID']
            # PendingTransaction.objects.create(
            #     user=current_request.user,
            #     merchant_re_id=merchant_r_id,
            #     checkout_re_id=checkout_r_id,
            #     amount=amount,
            #     phonenumber="+" + phonenumber
            # ).save()

            # messages.warning(current_request, 'Request has been sent! On the Mpesa prompt triggered enter your pin')
            return HttpResponse('Ok')
        else:
            # Notify user of an error in making stk push request
            return HttpResponse


@csrf_exempt
def call_back(request):
    # TODO: Check if request is from a safaricom server
    json_data = json.loads(request.body)

    result_code = json_data['Body']['stkCallback']['ResultCode']
    merchant_re_id = json_data['Body']['stkCallback']['MerchantRequestID']
    # if int(result_code) == 0:
    #     checkout_re_id = json_data['Body']['stkCallback']['CheckoutRequestID']
    #     amount = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value']
    #     reciept_no = json_data['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value']
    #     transaction_date = str(json_data['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'])
    #
    #     pending_transaction = PendingTransaction.objects.get(merchant_re_id=merchant_re_id)
    #     date = datetime.strptime(transaction_date, "%Y%m%d%H%M%S")
    #     date = date.replace(tzinfo=pytz.timezone('Africa/Nairobi'))
    #     CompleteTransactions.objects.create(
    #         user=pending_transaction.user,
    #         checkout_re_id=checkout_re_id,
    #         merchant_re_id=merchant_re_id,
    #         amount=amount,
    #         reciept_no=reciept_no,
    #         transaction_date=date
    #     )
    #
    #     pending_transaction.delete()
    # else:
    #     pending_transaction = PendingTransaction.objects.get(merchant_re_id=merchant_re_id)
    #     phone_number = pending_transaction.phone_number
    #     pending_transaction.delete()
    #
    #     MpesaErrorsHandler(str(result_code), [phone_number])

    return HttpResponse("Success")
