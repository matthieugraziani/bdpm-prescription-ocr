from unittest.mock import MagicMock, patch

import requests

from api.bdpm_client import check_api_status, search_medicine


@patch("api.bdpm_client.requests.get")
def test_search_medicine_success(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {"results": ["DOLIPRANE 1000 mg"]}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = search_medicine("doliprane")

    assert result == {"results": ["DOLIPRANE 1000 mg"]}


@patch("api.bdpm_client.requests.get")
def test_search_medicine_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("boom")

    result = search_medicine("doliprane")

    assert "error" in result


@patch("api.bdpm_client.requests.get")
def test_search_medicine_http_error(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error"
    )
    mock_get.return_value = mock_response

    result = search_medicine("doliprane")

    assert "error" in result


@patch("api.bdpm_client.requests.get")
def test_search_medicine_invalid_json(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.side_effect = ValueError("not json")
    mock_get.return_value = mock_response

    result = search_medicine("doliprane")

    assert "error" in result


@patch("api.bdpm_client.requests.get")
def test_check_api_status_up(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    assert check_api_status() is True


@patch("api.bdpm_client.requests.get")
def test_check_api_status_down(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("boom")

    assert check_api_status() is False