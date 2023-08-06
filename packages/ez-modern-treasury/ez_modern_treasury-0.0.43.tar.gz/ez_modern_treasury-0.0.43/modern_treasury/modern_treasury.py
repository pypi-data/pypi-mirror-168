from typing import Optional, List

import requests
from requests.auth import HTTPBasicAuth

from modern_treasury import AccountDetailsResponse, AccountDetailsRequest, PaymentOrderResponse
from modern_treasury.objects.exceptions import ModernTreasuryException
from modern_treasury.objects.request.counterparty import CounterPartyRequest
from modern_treasury.objects.request.expected_payment import ExpectedPaymentRequest
from modern_treasury.objects.request.external_account import ExternalAccountRequest
from modern_treasury.objects.request.incoming_payment_detail import IncomingPaymentDetailRequest
from modern_treasury.objects.request.internal_account import InternalAccountRequest
from modern_treasury.objects.request.payment_order import PaymentOrderRequest, UpdatePaymentOrderRequest
from modern_treasury.objects.request.routing_details import RoutingDetailsRequest
from modern_treasury.objects.request.virtual_account import VirtualAccountRequest
from modern_treasury.objects.response.connection import ConnectionResponse
from modern_treasury.objects.response.counterparty import CounterPartyResponse
from modern_treasury.objects.response.expected_payment import ExpectedPaymentResponse
from modern_treasury.objects.response.external_account import ExternalAccountResponse
from modern_treasury.objects.response.incoming_payment_detail import IncomingPaymentDetailResponse
from modern_treasury.objects.response.internal_account import InternalAccountResponse

from modern_treasury.objects.response.routing_details import RoutingDetailsResponse
from modern_treasury.objects.response.virtual_account import VirtualAccountResponse

INTERNAL_ACCOUNT_URL = 'https://app.moderntreasury.com/api/internal_accounts'
COUNTER_PARTIES_URL = 'https://app.moderntreasury.com/api/counterparties'
EXPECTED_PAYMENTS_URL = 'https://app.moderntreasury.com/api/expected_payments'
PAYMENT_ORDER_URL = 'https://app.moderntreasury.com/api/payment_orders'
VIRTUAL_ACCOUNT_URL = 'https://app.moderntreasury.com/api/virtual_accounts'
EXTERNAL_ACCOUNT_URL = 'https://app.moderntreasury.com/api/external_accounts'
LIST_INCOMING_PAYMENT_DETAIL_URL = 'https://app.moderntreasury.com/api/incoming_payment_details'
INCOMING_PAYMENT_DETAIL_URL = 'https://app.moderntreasury.com/api/simulations/incoming_payment_details/create_async'
LIST_CONNECTIONS_URL = 'https://app.moderntreasury.com/api/connections'


class ModernTreasury:
    def create(organization_id:str, api_key:str):
        return ModernTreasury(organization_id=organization_id, api_key=api_key)

    def __init__(self, organization_id: str, api_key: str):
        self.organization_id = organization_id
        self.api_key = api_key
        self.http_basic_auth = HTTPBasicAuth(username=self.organization_id, password=self.api_key)
        self.headers = {"Content-Type": "application/json"}

    def _post(self, url:str, payload: dict, idempotency_key: str = None) -> dict:
        headers = {**self.headers, "Idempotency-Key": idempotency_key} if idempotency_key else self.headers
        response = requests.post(url=url,
                                 auth=self.http_basic_auth,
                                 headers=headers,
                                 json=payload)
        if not response.ok:
            raise ModernTreasuryException(response.status_code, response.reason, url, response.json())
        return response.json()

    def _get(self, url:str, params = None) -> dict:
        response = requests.get(url=url,
                                auth=self.http_basic_auth,
                                headers=self.headers,
                                params=params)
        if not response.ok:
            raise ModernTreasuryException(response.status_code, response.reason, url, response.json())
        return response.json()

    def _patch(self, url:str, payload: dict) -> dict:
        response = requests.request("PATCH",
                                    url=url,
                                    json=payload,
                                    headers=self.headers,
                                    auth=self.http_basic_auth)
        if not response.ok:
            raise ModernTreasuryException(response.status_code, response.reason, url, response)
        return response.json()

    def _delete(self, url:str) -> dict:
        response = requests.request("DELETE",
                                    url=url,
                                    headers=self.headers,
                                    auth=self.http_basic_auth)
        if not response.ok:
            raise ModernTreasuryException(response.status_code, response.reason, url, response)

    # Counter Parties
    def get_counter_parties(self):
        return self._get(url=COUNTER_PARTIES_URL)

    def get_counterparty_account_by_name(self, name) -> Optional[CounterPartyResponse]:
        for account in self.get_counter_parties():
            mt_account = CounterPartyResponse(account)
            if mt_account.name == name:
                return mt_account
        return None

    def update_counterparty(self, counterparty_request: CounterPartyRequest, counterparty_id:str):
        payload = counterparty_request.to_json()
        self._patch(url=f'{COUNTER_PARTIES_URL}/{counterparty_id}', payload=payload)

    def list_counterparties(self, metadata: dict=None) -> List[Optional[CounterPartyResponse]]:
        querystring = {'page': '1', 'per_page': '100'}
        if metadata:
            for key, value in metadata.items():
                querystring[f'metadata[{str(key)}]'] = str(value)

        try:
            response = self._get(url=COUNTER_PARTIES_URL, params=querystring)
            return [CounterPartyResponse(counterparty) for counterparty in response]
        except:
            return []

    def delete_counterparty_by_id(self, id:str) -> bool:
        return self._delete(url=f'{COUNTER_PARTIES_URL}/{id}')

    def get_counterparty_account_by_id(self, id:str) -> CounterPartyResponse:
        return CounterPartyResponse(self._get(url=f'{COUNTER_PARTIES_URL}/{id}'))

    def create_counterparty_account(self, counterparty_request: CounterPartyRequest) -> CounterPartyResponse:
        return CounterPartyResponse(self._post(url=COUNTER_PARTIES_URL, payload=counterparty_request.to_json(), idempotency_key=counterparty_request.idempotency_key))

    # external account
    def update_external_account(self, external_account_request: ExternalAccountRequest,
                                external_account_id:str) -> ExternalAccountResponse:
        payload = external_account_request.to_json()
        result = self._patch(url=f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}',
                             payload=payload)
        if result:
            return ExternalAccountResponse(result)
        return None

    # account details
    def delete_account_details(self, external_account_id:str, account_details_id:str):
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}/account_details/{account_details_id}'
        result = self._delete(url=url)
        return result

    def create_account_details(self, account_details: AccountDetailsRequest,
                               external_account_id: str) -> AccountDetailsResponse:
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}/account_details'
        payload = account_details.to_json()
        return AccountDetailsResponse(self._post(url=url, payload=payload, idempotency_key=account_details.idempotency_key))

    # routing details
    def get_routing_details_by_id(self, external_account_id, routing_details_id):
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}/routing_details/{routing_details_id}'
        return self._get(url=url)

    def list_routing_details(self, external_account_id):
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}/routing_details/'
        return self._get(url=url)

    def delete_routing_details(self, external_account_id:str, routing_details_id:str):
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}/routing_details/{routing_details_id}'
        result = self._delete(url=url)
        return result

    def create_routing_details(self, routing_details: RoutingDetailsRequest,
                               external_account_id: str) -> RoutingDetailsResponse:
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}/routing_details'
        payload = routing_details.to_json()
        return RoutingDetailsResponse(self._post(url=url, payload=payload, idempotency_key=routing_details.idempotency_key))

    # Internal Accounts
    def get_internal_accounts(self, per_page=None, page=None):
        params = {}
        if per_page:
            params.update({"per_page": per_page})
        if page:
            params.update({"page": page})
        result = self._get(url=INTERNAL_ACCOUNT_URL, params=params if params else None)

        internal_accounts = []
        for account in result:
            internal_accounts.append(InternalAccountResponse(account))
        return internal_accounts

    def get_internal_account_by_id(self, id:str) -> Optional[InternalAccountResponse]:
        if id:
            result = self._get(url=f'{INTERNAL_ACCOUNT_URL}/{id}')
            return InternalAccountResponse(result)
        else:
            raise Exception("id cannot be an empty string")

    # External Accounts
    def create_external_account(self, external_account_request: ExternalAccountRequest):
        response = self._post(url=EXTERNAL_ACCOUNT_URL, payload=external_account_request.to_json(), idempotency_key=external_account_request.idempotency_key)
        return ExternalAccountResponse(response)

    def delete_external_account(self, external_account_id:str):
        url = f'{EXTERNAL_ACCOUNT_URL}/{external_account_id}'
        result = self._delete(url=url)
        return result

    # Expected Payments
    def create_expected_payment(self, expected_payment_request: ExpectedPaymentRequest) -> ExpectedPaymentResponse:
        response = self._post(url=EXPECTED_PAYMENTS_URL, payload=expected_payment_request.to_json(), idempotency_key=expected_payment_request.idempotency_key)
        return ExpectedPaymentResponse(response)

    def get_expected_payment_by_id(self, id:str) -> Optional[ExpectedPaymentResponse]:
        result = requests.get(url=f'{EXPECTED_PAYMENTS_URL}/{id}', auth=self.http_basic_auth)
        return ExpectedPaymentResponse(result.json())

    def update_expected_payment(self, id:str, expected_payment_request: ExpectedPaymentRequest) -> ExpectedPaymentResponse:
        response = self._patch(url=f'{EXPECTED_PAYMENTS_URL}/{id}', payload=expected_payment_request.to_json())
        return ExpectedPaymentResponse(response)

    # Payment Orders
    def create_payment_order(self, payment_order_request: PaymentOrderRequest) -> PaymentOrderResponse:
        response = self._post(url=PAYMENT_ORDER_URL, payload=payment_order_request.to_json(), idempotency_key=payment_order_request.idempotency_key)
        return PaymentOrderResponse(response)

    def get_payment_order(self, id):
        result = self._get(url=f'{PAYMENT_ORDER_URL}/{id}')
        return PaymentOrderResponse(result)

    def list_payment_orders(self, metadata: dict=None) -> List[Optional[PaymentOrderResponse]]:
        querystring = {}
        if metadata:
            for key, value in metadata.items():
                querystring[f'metadata[{str(key)}]'] = str(value)
        try:
            response = self._get(url=PAYMENT_ORDER_URL, params=querystring)
            return [PaymentOrderResponse(payment_order) for payment_order in response]
        except:
            return []
    
    def update_payment_order(self, id, payment_order_request: UpdatePaymentOrderRequest) -> PaymentOrderResponse:
        response = self._patch(url=f"{PAYMENT_ORDER_URL}/{id}", payload=payment_order_request.to_json())
        return PaymentOrderResponse(response)

    # Virtual Account
    def list_virtual_accounts(self, metadata: dict=None) -> List[Optional[VirtualAccountResponse]]:
        querystring = {}
        if metadata:
            for key, value in metadata.items():
                querystring[f'metadata[{str(key)}]'] = str(value)
        try:
            response = self._get(url=VIRTUAL_ACCOUNT_URL, params=querystring)
            return [VirtualAccountResponse(virtual_account) for virtual_account in response]
        except:
            return []

    def create_virtual_account(self, virtual_account_request: VirtualAccountRequest):
        response = self._post(url=VIRTUAL_ACCOUNT_URL,
                              payload=virtual_account_request.to_json(),
                              idempotency_key=virtual_account_request.idempotency_key)
        return VirtualAccountResponse(response)

    def get_virtual_account_by_id(self, id:str):
        result = requests.get(url=f'{VIRTUAL_ACCOUNT_URL}/{id}', auth=self.http_basic_auth)
        return VirtualAccountResponse(result.json())

    def post_incoming_payment_detail(self, incoming_payment_detail_request: IncomingPaymentDetailRequest)\
            -> IncomingPaymentDetailResponse:
        response = self._post(url=INCOMING_PAYMENT_DETAIL_URL,
                              payload=incoming_payment_detail_request.to_json(),
                              idempotency_key=incoming_payment_detail_request.idempotency_key)
        return IncomingPaymentDetailResponse(response)

    def list_incoming_payment_detail(self, virtual_account_id: str = None) -> List[Optional[CounterPartyResponse]]:
        querystring = {}
        if virtual_account_id:
                querystring[f'virtual_account_id'] = virtual_account_id
        try:
            response = self._get(url=LIST_INCOMING_PAYMENT_DETAIL_URL, params=querystring)
            return [IncomingPaymentDetailResponse(payment_order) for payment_order in response]
        except:
            return []

    def list_connections(self, vendor_customer_id: Optional[str] = None, entity: Optional[str] = None) -> List[ConnectionResponse]:
        querystring = {
            "vendor_customer_id": vendor_customer_id,
            "entity": entity,
        }
        response = self._get(LIST_CONNECTIONS_URL, params=querystring)
        return [ConnectionResponse(connection) for connection in response]

    def create_internal_account(self, internal_account_request: InternalAccountRequest) -> InternalAccountResponse:
        response = self._post(
            url=INTERNAL_ACCOUNT_URL,
            payload=internal_account_request.to_json(),
            idempotency_key=internal_account_request.idempotency_key)
        return InternalAccountResponse(response)

    def get_connection_by_vendor(self, vendor_name: Optional[str] = None, vendor_id: Optional[str] = None) -> Optional[ConnectionResponse]:
        connections = self.list_connections()
        if vendor_name:
            connections = filter(lambda connection: connection.vendor_name == vendor_name, connections)
        if vendor_id:
            connections = filter(lambda connection: connection.vendor_id == vendor_id, connections)
        return next(iter(connections), None)
