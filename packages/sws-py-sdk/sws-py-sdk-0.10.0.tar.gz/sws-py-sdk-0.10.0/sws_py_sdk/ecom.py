""" This file exposes endpoints from the SWS Ecom Service
"""

from requests.auth import HTTPBasicAuth

from sws_py_sdk.service import Service


class Ecom(Service):

    def __init__(self, sws):
        super().__init__(sws)
        self.service_uri = sws.service_uris['ecom']

    def add_payment_method(self, nonce=None, device_data=None, billing_address_id=None):
        """ Add a payment method to the authenticated client user.
            nonce: str
                One-time-use reference to payment information provided by the user.
            device_data: str
                User device information.
            billing_address_id: str
                The two-letter value for an address associated with a specific customer ID.
        """
        return self.fetch(
            auth='bearer',
            endpoint='/api/v1/me/paymentmethods' if self.sws.user_id == 0 else '/api/v1/users/' +
            str(self.sws.user_id) + '/paymentmethods',
            body={"nonce": nonce, "device_data": device_data, "billing_address_id": billing_address_id},
            method='POST'
        )

    def add_plan_change_request(self, subscription_id, catalog_product_id):
        """ Create a new plan change that belongs to the authenticated client user.

            subscription_id: int
                Id of the subscription that is requesting change
            catalog_product_id: int
                The id of the product that the subscription wants to change to
        """
        endpoint = '/api/v1/me/' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "subscriptions/" + subscription_id + "/planchanges"

        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            body={"catalog_product_id": catalog_product_id},
            method='POST'
        )

    def get_subscriptions(self, subscription_id=''):
        """ Get subscriptions owned by a user
        """
        endpoint = "/api/v1/me/subscriptions" if self.sws.user_id == 0 else "/api/v1/users/" + \
            str(self.sws.user_id) + "/subscriptions"
        if subscription_id != '':
            endpoint += "/" + str(subscription_id)
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            method="GET"
        )

    def get_invoice(self, order_id, invoice_id, accept='application/json'):
        """ Gets a specific invoice for an order

            order_id: int
                ID of the order
            invoice_id: int
                ID of the invoice
            accept: string
                Accept header, can be JSON, PDF or HTML
        """
        prefix = "/api/v1/me" if self.sws.user_id == 0 else "/api/v1/users/" + str(self.sws.user_id)
        endpoint = f"{prefix}/orders/{order_id}/invoices/{invoice_id}"
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            method="GET",
            headers={'Accept': accept}
        )

    def get_orders(self, order_id=0):
        """ Get list of all orders created by the authenticated client user

            order_id: int
                ID of order
        """
        endpoint = "/api/v1/me" if self.sws.user_id == 0 else "/api/v1/users/" + str(self.sws.user_id)
        endpoint = endpoint + "/orders"
        if order_id != 0:
            endpoint = endpoint + "/" + str(order_id)
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            method="GET"
        )

    def get_payment_methods(self):
        """ Gets users payment methods
        """
        endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint += '/paymentmethods'

        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            method='GET'
        )

    def update_payment_methods(self, payment_token, nonce, device_data=None, billing_address_id=None):
        """ Update the payment method that belongs to the user

            payment_token: str
                Payment token string relating to user's payment method
            nonce: str
                One-time-use reference to payment information provided by the user.
            device_data: str
                User device information.
            billing_address_id: str
                The two-letter value for an address associated with a specific customer ID.
        """
        endpoint = '/api/v1/me/paymentmethods/' if self.sws.user_id == 0 else '/api/v1/users/' + \
            str(self.sws.user_id) + '/paymentmethods/'
        endpoint = endpoint + payment_token

        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            method='PUT',
            body={"nonce": nonce, "device_data": device_data, "billing_address_id": billing_address_id}
        )

    def update_plan_change(self, subscription_id, plan_change_id):
        """ Update an existing plan change

            subscription_id: str
                Subscripton ID
            plan_change_id: str
                The ID for the change request
        """
        endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "/subscriptions/" + subscription_id + "/planchanges/" + plan_change_id
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            method="PUT"
        )

    def update_subscription(self, subscription_id, number_of_billing_cycle=None, payment_method_token=None):
        """ Update a subscription owned by the user

            subscription_id: str
                Subscripton ID
            number_of_billing_cycle: int
                Number of billing cyles after which the subscription will expire.
            payment_method_token: str
                Token style identifier of the payment method
        """
        endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "/subscriptions/" + subscription_id
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            body={"number_of_billing_cycle": number_of_billing_cycle, "payment_method_token": payment_method_token},
            method="PUT"
        )

    def delete_payment_method(self, payment_method_token):
        """ Deletes the user's payment method for the given payment method token

            payment_method_token: str
                Token style identifier of the payment method
        """
        endpoint = endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "/paymentmethods/" + payment_method_token
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            method="DELETE"
        )

    def delete_subscription(self, subscription_id):
        """ Deletes the user's subscription for the given subscription id

            subscription_id: int
                Token style identifier of the payment method
        """
        endpoint = endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "/subscriptions/" + subscription_id
        return self.fetch(
            auth="bearer",
            endpoint=endpoint,
            method="DELETE"
        )

    def send_braintree_webhook(self, notification_kind, subscription_id):
        """ Sends a braintree webhook

            notification_kind: string
                Notification type
            subscription_id: string
                Subscription ID
        """
        endpoint = '/api/v1/webhook/braintree'
        return self.fetch(
            auth=HTTPBasicAuth(username=self.sws.app_id, password=self.sws.secret),
            body={"notification_kind": notification_kind, "subscription_id": subscription_id},
            endpoint=endpoint,
            method="POST"
        )

    def create_promotion(self, name, description, coupon_based, enabled, starts_at=None, ends_at=None):
        """ Create a promotion

            name: string
            description: string
            starts_at: string
                datetime format
            ends_at: string
                datetime format
            coupon_based: boolean
            endabled: boolean
        """
        endpoint = '/api/v1/promotions'
        return self.fetch(
            auth='bearer',
            body={
                "name": name,
                "description": description,
                "starts_at": starts_at,
                "ends_at": ends_at,
                "coupon_based": coupon_based,
                "enabled": enabled
            },
            endpoint=endpoint,
            method="POST"
        )

    def create_promotion_coupons(
        self,
        promotion_id,
        usage_limit=None,
        usage_limit_per_user=None,
        expires_at=None,
        coupon_code=None
    ):
        """ Create a promotion coupon

            promotion_id: int
            usage_limit: int
            usage_limit_per_user: int
            expires_at: string
                datetime format
            coupon_code: string
        """
        endpoint = f"/api/v1/promotions/{promotion_id}/coupons"
        return self.fetch(
            auth='bearer',
            body={
                "usage_limit": usage_limit,
                "usage_limit_per_user": usage_limit_per_user,
                "expires_at": expires_at,
                "coupon_code": coupon_code
            },
            endpoint=endpoint,
            method="POST"
        )

    def create_promotion_rule(
        self,
        promotion_id,
        product_type_id,
        discount_percentage=None,
        discount_fixed_amount=None,
        pre_condition_product_id=None,
        braintree_discount_id=None,
        subscription_promotion_expires=None
    ):
        """ Create a promotion rule
            promotion_id: int
            product_type_id: int
            discount_percentage: float
            discount_fixed_amount: float
            pre_condition_product_id: int
            braintree_discount_id: string
            subscription_promotion_expires: int
        """
        endpoint = f"/api/v1/promotions/{promotion_id}/rules"
        return self.fetch(
            auth='bearer',
            body={
                "product_type_id": product_type_id,
                "discount_percentage": discount_percentage,
                "discount_fixed_amount": discount_fixed_amount,
                "pre_condition_product_id": pre_condition_product_id,
                "braintree_discount_id": braintree_discount_id,
                "subscription_promotion_expires": subscription_promotion_expires
            },
            endpoint=endpoint,
            method="POST"
        )

    def delete_promotion(self, promotion_id):
        """ Deletes a promotion

            promotion_id: int
        """
        endpoint = f"/api/v1/promotions/{promotion_id}"
        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            method="DELETE"
        )

    def delete_promotion_coupon(self, promotion_id, coupon_code):
        """ Deletes a promotion coupon

            promotion_id: int
        """
        endpoint = f"/api/v1/promotions/{promotion_id}/coupons/{coupon_code}"
        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            method="DELETE"
        )

    def create_voucher(self, voucher_type_id, batch_id):
        """Create a vouchers for the provided voucher type

            voucher_type_id: int
            batch_id: string
        """
        endpoint = '/api/v1/vouchers'
        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            body={
                "voucher_type_id": voucher_type_id,
                "batch_id": batch_id
            },
            method="POST"
        )

    def assign_voucher(self, voucher_id):
        """Assign a voucher to a user

            voucher_id: string
        """
        endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "/vouchers"
        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            body={
                "voucher_id": voucher_id
            },
            method="POST"
        )

    def redeem_voucher(self, voucher_id):
        """ Redeem a voucher to the authenticated client user

            voucher_id: string
        """
        endpoint = '/api/v1/me' if self.sws.user_id == 0 else '/api/v1/users/' + str(self.sws.user_id)
        endpoint = endpoint + "/vouchers/" + voucher_id

        return self.fetch(
            auth='bearer',
            endpoint=endpoint,
            method="PUT"
        )
