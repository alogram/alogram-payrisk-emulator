# coding: utf-8

from typing import Any, Optional  # noqa: F401

from fastapi.testclient import TestClient
from payrisk_base_server.models.account_check_request import (  # noqa: F401
    AccountCheckRequest,
)
from payrisk_base_server.models.check_request import CheckRequest  # noqa: F401
from payrisk_base_server.models.decision_response import DecisionResponse  # noqa: F401
from payrisk_base_server.models.kyc_check_request import KycCheckRequest  # noqa: F401
from payrisk_base_server.models.payment_event import PaymentEvent  # noqa: F401
from payrisk_base_server.models.problem import Problem  # noqa: F401
from payrisk_base_server.models.scores_success_response import (  # noqa: F401
    ScoresSuccessResponse,
)
from payrisk_base_server.models.signals_request import SignalsRequest  # noqa: F401
from pydantic import Field, StrictStr, field_validator  # noqa: F401
from typing_extensions import Annotated  # noqa: F401


def test_risk_check(client: TestClient):
    """Test case for risk_check

    Synchronous fraud decision for a purchase
    """
    # check_request = {
    #    "payment_intent_id": "pi_0123456789abcdef0123456789abcdef",
    #    "entities": {
    #        "tenant_id": "tid_acme_01",
    #        "client_id": "cid_merchant_42",
    #        "end_customer_id": "ecid_shopper_9f",
    #        "payment_instrument_id": "tok_abcdef1234567890",
    #        "device_id": "did_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    #        "session_id": "sid_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    #        "email_hash": "sha256_...",
    #        "phone_hash": "sha256_...",
    #    },
    #    "identity": {
    #        "email": "shopper@example.com",
    #        "phone": "+1 (415) 555-2671",
    #        "shipping_address": {
    #            "line1": "123 Market Street",
    #            "city": "San Francisco",
    #            "region": "CA",
    #            "postal_code": "94103",
    #            "country": "US",
    #        },
    #        "billing_address": {
    #            "line1": "123 Market Street",
    #            "city": "San Francisco",
    #            "region": "CA",
    #            "postal_code": "94103",
    #            "country": "US",
    #        },
    #    },
    #    "purchase": {"event_type": "purchase"},
    # }

    # headers = {
    #    "x_trace_id": "x_trace_id_example",
    #    "x_idempotency_key": "x_idempotency_key_example",
    #    "ApiKey": "special-key",
    #    "Authorization": "Bearer special-key",
    # }
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/v1/risk/check",
    #    headers=headers,
    #    json=check_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_ingest_payment_event(client: TestClient):
    """Test case for ingest_payment_event

    Ingest payment lifecycle events (authorization, capture, settlement, refund, dispute, chargeback,
    chargeback_outcome).
    """
    # payment_event = {
    #    "payment_intent_id": "pi_0123456789abcdef0123456789abcdef",
    #    "event_type": "authorization",
    #    "timestamp": "2023-12-14T15:45:30.123Z",
    # }

    # headers = {
    #    "x_trace_id": "x_trace_id_example",
    #    "x_idempotency_key": "x_idempotency_key_example",
    #    "ApiKey": "special-key",
    #    "Authorization": "Bearer special-key",
    # }
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/v1/events",
    #    headers=headers,
    #    json=payment_event,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_ingest_signals(client: TestClient):
    """Test case for ingest_signals

    Ingest non-payment signals (account or interaction) for modeling
    """
    # signals_request = {
    #    "signal_type": "account",
    #    "entities": {
    #        "tenant_id": "tid_alogram_01",
    #        "end_customer_id": "ecid_shopper_9f",
    #    },
    #    "account": {
    #        "email": "someemail@example-emails.com",
    #        "timestamp": "2023-12-14T15:45:30.123Z",
    #        "device_info": {
    #            "fingerprint": "fp_5f4dcc3b5aa765d61d8327deb882cf99",
    #            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    #            "ip": {"ip_address": "192.168.1.100", "country": "US"},
    #        },
    #    },
    # }

    # headers = {
    #    "x_trace_id": "x_trace_id_example",
    #    "x_idempotency_key": "x_idempotency_key_example",
    #    "ApiKey": "special-key",
    #    "Authorization": "Bearer special-key",
    # }
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/v1/signals",
    #    headers=headers,
    #    json=signals_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_get_fraud_scores(client: TestClient):
    """Test case for get_fraud_scores

    Retrieve fraud scores for a customer
    """
    # params = [
    #    ("start_time", "start_time_example"),
    #    ("end_time", "end_time_example"),
    #    ("page_size", 50),
    #    ("page_token", "page_token_example"),
    # ]
    # headers = {
    #    "x_trace_id": "x_trace_id_example",
    #    "x_idempotency_key": "x_idempotency_key_example",
    #    "ApiKey": "special-key",
    #    "Authorization": "Bearer special-key",
    # }
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/v1/scores/{tenantId}".format(tenantId='tenant_id_example'),
    #    headers=headers,
    #    params=params,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_health_check(client: TestClient):
    """Test case for health_check

    Health check for the service
    """

    # headers = {}
    # uncomment below to make a request
    # response = client.request(
    #    "GET",
    #    "/v1/health",
    #    headers=headers,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_account_risk_check(client: TestClient):
    """Test case for account_risk_check

    Synchronous fraud decision for account/session events (signup, login, settings)
    """
    # account_check_request = {
    #    "event_subtype": "signup",
    #    "entities": {
    #        "client_id": "cid_merchant_42",
    #        "email_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "shipping_address_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "tenant_id": "tid_acme_01",
    #        "phone_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "payment_instrument_id": "tok_abcdef1234567890",
    #        "end_customer_id": "ecid_shopper_9f",
    #        "session_id": "sid_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    #        "email_domain_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "device_id": "did_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    #        "billing_address_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "member_id": "mid_ops_27",
    #    },
    #    "interaction": {
    #        "location_id": "loc_1234",
    #        "interaction_type": "login",
    #        "timestamp": "2023-12-14T15:45:30.123Z",
    #        "device_info": {
    #            "fingerprint": "fp_5f4dcc3b5aa765d61d8327deb882cf99",
    #            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    #            "ip": {"ip_address": "192.168.1.100", "country": "US"},
    #        },
    #    },
    #    "account": {
    #        "email": "someemail@example-emails.com",
    #        "phone": "+1 (415) 555-2671",
    #        "timestamp": "2023-12-14T15:45:30.123Z",
    #        "device_info": {
    #            "fingerprint": "fp_5f4dcc3b5aa765d61d8327deb882cf99",
    #            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    #            "ip": {"ip_address": "192.168.1.100", "country": "US"},
    #        },
    #        "metadata": {"loyalty_tier": "gold"},
    #    },
    # }

    # headers = {
    #    "x_trace_id": "x_trace_id_example",
    #    "x_idempotency_key": "x_idempotency_key_example",
    #    "ApiKey": "special-key",
    #    "Authorization": "Bearer special-key",
    # }
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/v1/risk/account/check",
    #    headers=headers,
    #    json=account_check_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200


def test_kyc_risk_check(client: TestClient):
    """Test case for kyc_risk_check

    Synchronous decision for KYC/identity verification
    """
    # kyc_check_request = {
    #    "event_subtype": "pre_kyc_check",
    #    "kyc": {
    #        "result": "passed",
    #        "country": "US",
    #        "reason_codes": ["HIGH_VALUE", "HIGH_VALUE"],
    #        "metadata": '{"key1=value1":null,"key2=value2":null}',
    #        "provider": "onfido",
    #        "document_type": "national_id",
    #    },
    #    "entities": {
    #        "client_id": "cid_merchant_42",
    #        "email_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "shipping_address_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "tenant_id": "tid_acme_01",
    #        "phone_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "payment_instrument_id": "tok_abcdef1234567890",
    #        "end_customer_id": "ecid_shopper_9f",
    #        "session_id": "sid_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    #        "email_domain_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "device_id": "did_a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
    #        "billing_address_hash": "sha256_abcdef1234567890abcdef1234567890abcdef1234567890",
    #        "member_id": "mid_ops_27",
    #    },
    #    "account": {
    #        "email": "someemail@example-emails.com",
    #        "phone": "+1 (415) 555-2671",
    #        "timestamp": "2023-12-14T15:45:30.123Z",
    #        "device_info": {
    #            "fingerprint": "fp_5f4dcc3b5aa765d61d8327deb882cf99",
    #            "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    #            "ip": {"ip_address": "192.168.1.100", "country": "US"},
    #        },
    #        "metadata": {"loyalty_tier": "gold"},
    #    },
    # }

    # headers = {
    #    "x_trace_id": "x_trace_id_example",
    #    "x_idempotency_key": "x_idempotency_key_example",
    #    "ApiKey": "special-key",
    #    "Authorization": "Bearer special-key",
    # }
    # uncomment below to make a request
    # response = client.request(
    #    "POST",
    #    "/v1/risk/kyc/check",
    #    headers=headers,
    #    json=kyc_check_request,
    # )

    # uncomment below to assert the status code of the HTTP response
    # assert response.status_code == 200
