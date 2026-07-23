import pytest
from unittest.mock import MagicMock, patch
import requests_mock
from services import AzureOCRService, OpenAIService

class TestAzureOCRService:
    @pytest.fixture
    def service(self):
        return AzureOCRService(endpoint="https://test.cognitiveservices.azure.com", api_key="test-key")

    def test_init_adds_trailing_slash(self):
        service = AzureOCRService(endpoint="https://test.cognitiveservices.azure.com", api_key="test-key")
        assert service.endpoint.endswith("/")

    def test_analyze_image_success(self, service, requests_mock):
        image_data = b"fake_image_data"

        # Mock initial POST request
        requests_mock.post(
            f"{service.endpoint}vision/v3.2/read/analyze",
            status_code=202,
            headers={"Operation-Location": "https://test.cognitiveservices.azure.com/vision/v3.2/read/analyzeResults/123"}
        )

        # Mock polling GET request (first pending, then succeeded)
        requests_mock.get(
            "https://test.cognitiveservices.azure.com/vision/v3.2/read/analyzeResults/123",
            [
                {"json": {"status": "running"}, "status_code": 200},
                {"json": {
                    "status": "succeeded",
                    "analyzeResult": {
                        "readResults": [
                            {
                                "lines": [
                                    {"text": "Hello"},
                                    {"text": "World"}
                                ]
                            }
                        ]
                    }
                }, "status_code": 200}
            ]
        )

        with patch("services.POLL_INTERVAL_SECONDS", 0):
            result = service.analyze_image(image_data)
        assert result == "Hello\nWorld"

    def test_analyze_image_initial_failure(self, service, requests_mock):
        requests_mock.post(
            f"{service.endpoint}vision/v3.2/read/analyze",
            status_code=400
        )

        with pytest.raises(Exception, match="Request failed with status 400"):
            service.analyze_image(b"data")

    def test_analyze_image_processing_failed(self, service, requests_mock):
        requests_mock.post(
            f"{service.endpoint}vision/v3.2/read/analyze",
            status_code=202,
            headers={"Operation-Location": "https://test.cognitiveservices.azure.com/vision/v3.2/read/analyzeResults/123"}
        )

        requests_mock.get(
            "https://test.cognitiveservices.azure.com/vision/v3.2/read/analyzeResults/123",
            json={"status": "failed"}
        )

        with patch("services.POLL_INTERVAL_SECONDS", 0):
            with pytest.raises(Exception, match="Failed to process the image"):
                service.analyze_image(b"data")

    def test_rejects_non_https_endpoint(self):
        with pytest.raises(ValueError, match="valid HTTPS URL"):
            AzureOCRService(endpoint="http://example.com", api_key="test-key")

    def test_rejects_empty_image(self, service):
        with pytest.raises(ValueError, match="cannot be empty"):
            service.analyze_image(b"")

    def test_analyze_image_requires_operation_url(self, service, requests_mock):
        requests_mock.post(
            f"{service.endpoint}vision/v3.2/read/analyze",
            status_code=202
        )

        with pytest.raises(Exception, match="operation URL"):
            service.analyze_image(b"data")


class TestOpenAIService:
    @pytest.fixture
    def service(self):
        return OpenAIService(api_key="test-key")

    def test_get_response_technical(self, service):
        # Mock the client
        service.client = MagicMock()

        # Mock question type detection
        mock_type_response = MagicMock()
        mock_type_response.choices[0].message.content = "technical"

        # Mock answer generation
        mock_answer_response = MagicMock()
        mock_answer_response.choices[0].message.content = "Technical Answer"

        service.client.chat.completions.create.side_effect = [
            mock_type_response,
            mock_answer_response
        ]

        response = service.get_response("What is Python?")

        assert response == "Technical Answer"
        assert service.client.chat.completions.create.call_count == 2

        # Verify system prompt contains "technical" instructions
        call_args = service.client.chat.completions.create.call_args_list[1]
        assert "technical" in call_args[1]['messages'][0]['content']

    def test_get_response_behavioral(self, service):
        service.client = MagicMock()

        mock_type_response = MagicMock()
        mock_type_response.choices[0].message.content = "behavioral"

        mock_answer_response = MagicMock()
        mock_answer_response.choices[0].message.content = "STAR Answer"

        service.client.chat.completions.create.side_effect = [
            mock_type_response,
            mock_answer_response
        ]

        response = service.get_response("Tell me about a time...")

        assert response == "STAR Answer"

        # Verify system prompt contains "behavioral" instructions
        call_args = service.client.chat.completions.create.call_args_list[1]
        assert "behavioral" in call_args[1]['messages'][0]['content']

    def test_get_response_error(self, service):
        service.client = MagicMock()
        service.client.chat.completions.create.side_effect = Exception("API Error")

        with pytest.raises(Exception, match="Error generating response: API Error"):
            service.get_response("Question")
