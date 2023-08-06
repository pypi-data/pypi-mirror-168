import pytest
import responses
from freezegun import freeze_time
from requests.exceptions import HTTPError
from responses import matchers

from resistant_documents_client.base import ResistantApiException, DEFAULT_RETRY
from resistant_documents_client.client import ResistantDocumentsClient
from resistant_documents_client.model import AnalysisFeedback

CLIENT_ID = "client1"
CLIENT_SECRET = "client_secret"
TOKEN_URL = "https://get.token.com/v1/token"
ACCESS_TOKEN = "abc"
HEADERS = {"Authorization": f"Bearer {ACCESS_TOKEN}"}

API_URL = "https://api.endpoint"
ENDPOINTS = ["fraud", "quality", "content", "decision"]


@pytest.fixture
def client_mock():
    with responses.RequestsMock() as m:
        m.post(TOKEN_URL, json={"expires_in": 3600, "access_token": ACCESS_TOKEN})
        client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET, TOKEN_URL, API_URL)
        yield client, m


def test_token_refreshed_correctly():
    fraud_result = {"status_code": 200, "score": "HIGH_RISK"}
    with freeze_time() as frozen_datetime:
        with responses.RequestsMock() as m:
            token_resp = m.post(TOKEN_URL, json={"expires_in": 3600, "access_token": ACCESS_TOKEN})
            fraud_url = f'{API_URL}/v2/submission/id/fraud'
            fraud_resp = m.get(fraud_url, match=[matchers.header_matcher(headers=HEADERS)], json=fraud_result)

            client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET, TOKEN_URL, API_URL)

            for _ in range(3):
                assert fraud_result == client.fraud("id")
            assert token_resp.call_count == 1
            assert fraud_resp.call_count == 3
            frozen_datetime.tick(3700)

            assert fraud_result == client.fraud("id")
            assert token_resp.call_count == 2
            assert fraud_resp.call_count == 4


def test_submit(client_mock):
    client, m = client_mock
    desired_id = "id"
    submit_resp = m.post(
        f"{API_URL}/v2/submission",
        json={"upload_url": "https://test.upload/data", "submission_id": desired_id},
        match=[
            matchers.header_matcher(headers=HEADERS),
            matchers.json_params_matcher({'pipeline_configuration': 'ONLY_QUALITY', 'query_id': 'query_1', 'enable_decision': True})
        ]
    )
    upload_resp = m.put("https://test.upload/data", status=200)
    assert client.submit(b"abc", "query_1", "ONLY_QUALITY", enable_decision=True) == desired_id
    assert submit_resp.call_count == 1
    assert upload_resp.call_count == 1


@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_endpoint_returns_data(client_mock, endpoint_name):
    client, m = client_mock
    result = {"message": "ok"}

    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', match=[matchers.header_matcher(headers=HEADERS)], json=result)
    assert result == getattr(client, endpoint_name)("id")


@pytest.mark.parametrize("error_status", [429, 500, 502, 503, 504])
@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_endpoint_retries_on_retryable_errors(client_mock, endpoint_name, error_status):
    client, m = client_mock
    result = {"message": "ok"}
    for _ in range(DEFAULT_RETRY.total):
        m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', match=[matchers.header_matcher(headers=HEADERS)], status=error_status)
    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', match=[matchers.header_matcher(headers=HEADERS)], json=result)
    assert result == getattr(client, endpoint_name)("id")


def test_submit_endpoint_retries(client_mock):
    client, m = client_mock
    m.post(f"{API_URL}/v2/submission", status=500, match=[matchers.header_matcher(headers=HEADERS)])
    m.post(f"{API_URL}/v2/submission", status=500, match=[matchers.header_matcher(headers=HEADERS)])
    m.post(f"{API_URL}/v2/submission", json={"upload_url": "https://test.upload/data", "submission_id": "id"}, match=[matchers.header_matcher(headers=HEADERS)])
    m.put("https://test.upload/data", status=200)
    assert client.submit(b"abc", "query_1", "ONLY_QUALITY") == "id"


@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_poll_retries(client_mock, endpoint_name):
    client, m = client_mock
    result = {"message": "ok"}

    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', status=404)
    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', status=404)
    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', json=result)
    assert result == getattr(client, endpoint_name)("id")


@pytest.mark.parametrize("endpoint_name", ENDPOINTS)
def test_results_throws_exception_when_no_data_exists(client_mock, endpoint_name):
    client, m = client_mock
    m.get(f'{API_URL}/v2/submission/id/{endpoint_name}', status=404, match=[matchers.header_matcher(headers=HEADERS)])
    with pytest.raises(RuntimeError):
        getattr(client, endpoint_name)("id", max_num_retries=2)


def test_fraud_presign(client_mock):
    client, m = client_mock
    m.get(f'{API_URL}/v2/submission/id/fraud', status=400, match=[matchers.header_matcher(headers=HEADERS)])
    presign_s3_url = "https://s3.download.aws.com/some_object"
    m.get(
        f'{API_URL}/v2/submission/id/fraud',
        status=200,
        json={"download_url": presign_s3_url},
        match=[
            matchers.header_matcher(headers=HEADERS),
            matchers.query_param_matcher({"presign": True}),
        ]
    )
    response = {"status": "SUCCESS"}
    m.get(presign_s3_url, json=response)

    act_response = client.fraud("id", 1)
    assert act_response == response


def test_client_proxy():
    no_proxy_client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET)
    assert no_proxy_client._api_session.proxies == {}
    assert no_proxy_client._s3_session.proxies == {}

    proxy_url = "proxy-url"
    proxy_client = ResistantDocumentsClient(CLIENT_ID, CLIENT_SECRET, proxy=proxy_url)
    assert proxy_client._api_session.proxies == {"https": proxy_url}
    assert proxy_client._s3_session.proxies == {"https": proxy_url}


@pytest.mark.parametrize("status, body, exception, message", [
    (200, {"analysis_feedback": "CORRECT", "comment": "comment", "updated": "2022-06-09T10:48:00Z"}, None, None),
    (404, None, None, None),
    (555, None, HTTPError, "555 Server Error"),
])
def test_feedback_get(client_mock, status, body, exception, message):
    client, m = client_mock
    m.get(f"{API_URL}/v2/submission/id/feedback", match=[matchers.header_matcher(headers=HEADERS)], status=status, json=body)

    if exception:
        with pytest.raises(exception, match=message):
            client.feedback("id")
    else:
        assert client.feedback("id") == body


@pytest.mark.parametrize("status, body, exception, message", [
    (200, {"analysis_feedback": "CORRECT", "comment": "comment", "updated": "2022-06-09T10:48:00Z"}, None, None),
    (404, None, ResistantApiException, "Add feedback failed, submission id not found"),
    (555, None, HTTPError, "555 Server Error"),
])
def test_feedback_put(client_mock, status, body, exception, message):
    client, m = client_mock
    put_resp = m.put(
        f"{API_URL}/v2/submission/id/feedback",
        match=[
            matchers.header_matcher(headers=HEADERS),
            matchers.json_params_matcher({"analysis_feedback": "CORRECT", "comment": "comment"})
        ],
        status=status,
        json=body
    )

    if exception:
        with pytest.raises(exception, match=message):
            client.add_feedback("id", AnalysisFeedback.CORRECT, "comment")
    else:
        assert client.add_feedback("id", AnalysisFeedback.CORRECT, "comment") == body
    assert put_resp.call_count == 1


@pytest.mark.parametrize("status, exception, message", [
    (204, None, None),
    (404, ResistantApiException, "Delete submission failed, submission id not found"),
    (409, ResistantApiException, "Delete submission failed, submission id not ready"),
    (555, HTTPError, "555 Server Error"),  # cannot be 500 as 500 error is retried
])
def test_delete(client_mock, status, exception, message):
    client, m = client_mock
    m.delete(f"{API_URL}/v2/submission/id", match=[matchers.header_matcher(headers=HEADERS)], status=status)

    if exception:
        with pytest.raises(exception, match=message):
            client.delete("id")
    else:
        assert client.delete("id") is None
