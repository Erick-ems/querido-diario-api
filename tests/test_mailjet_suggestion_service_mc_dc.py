import pytest
from unittest.mock import Mock
from mailjet_rest import Client
from suggestions.model import Suggestion
from suggestions.service import MailjetSuggestionService


@pytest.fixture
def mock_mailjet_client():
    client = Mock(spec=Client)
    client.send = Mock()
    client.send.create = Mock()
    return client


@pytest.fixture
def suggestion_service(mock_mailjet_client):
    return MailjetSuggestionService(
        mailjet_client=mock_mailjet_client,
        suggestion_sender_name="Sender Name",
        suggestion_sender_email="sender@example.com",
        suggestion_recipient_name="Recipient Name",
        suggestion_recipient_email="recipient@example.com",
        suggestion_mailjet_custom_id="custom_id",
    )


def test_add_suggestion_status_code_200_empty_errors(
    suggestion_service, mock_mailjet_client
):
    result = Mock()
    result.status_code = 200
    result.json.return_value = {"Messages": [{"Errors": []}]}
    mock_mailjet_client.send.create.return_value = result

    suggestion = Suggestion(
        name="John Doe",
        email_address="john.doe@example.com",
        content="This is a suggestion",
    )
    result = suggestion_service.add_suggestion(suggestion)

    assert result.success is True
    assert result.status == "Sent"


def test_add_suggestion_status_code_400_with_errors(
    suggestion_service, mock_mailjet_client
):
    result = Mock()
    result.status_code = 400
    result.json.return_value = {
        "Messages": [{"Errors": [{"ErrorMessage": "Invalid email"}]}]
    }
    mock_mailjet_client.send.create.return_value = result

    suggestion = Suggestion(
        name="John Doe",
        email_address="john.doe@example.com",
        content="This is a suggestion",
    )
    result = suggestion_service.add_suggestion(suggestion)

    assert result.success is False
    assert result.status == "Could not sent message: Invalid email"


def test_add_suggestion_status_code_150_with_errors(
    suggestion_service, mock_mailjet_client
):
    result = Mock()
    result.status_code = 150
    result.json.return_value = {
        "Messages": [{"Errors": [{"ErrorMessage": "Invalid email"}]}]
    }
    mock_mailjet_client.send.create.return_value = result

    suggestion = Suggestion(
        name="John Doe",
        email_address="john.doe@example.com",
        content="This is a suggestion",
    )
    result = suggestion_service.add_suggestion(suggestion)

    assert result.success is False
    assert result.status == "Could not sent message: Invalid email"


def test_add_suggestion_status_code_500_empty_errors(
    suggestion_service, mock_mailjet_client
):
    result = Mock()
    result.status_code = 500
    result.json.return_value = {"Messages": [{"Errors": []}]}
    mock_mailjet_client.send.create.return_value = result

    suggestion = Suggestion(
        name="John Doe",
        email_address="john.doe@example.com",
        content="This is a suggestion",
    )
    result = suggestion_service.add_suggestion(suggestion)

    assert result.success is False
    assert result.status == "Could not sent message: unknown error"
