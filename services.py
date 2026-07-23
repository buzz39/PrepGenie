import requests
import time
from openai import OpenAI
import httpx
from urllib.parse import urlparse


REQUEST_TIMEOUT = (5, 30)
POLL_INTERVAL_SECONDS = 1
POLL_TIMEOUT_SECONDS = 120

class AzureOCRService:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint.strip()
        self.api_key = api_key.strip()

        parsed_endpoint = urlparse(self.endpoint)
        if parsed_endpoint.scheme != "https" or not parsed_endpoint.netloc:
            raise ValueError("Azure Vision endpoint must be a valid HTTPS URL")
        if not self.api_key:
            raise ValueError("Azure Vision API key is required")

        # Ensure endpoint ends with '/'
        if not self.endpoint.endswith('/'):
            self.endpoint += '/'

    def analyze_image(self, image_data: bytes) -> str:
        """
        Analyzes the image data using Azure Computer Vision API and returns the extracted text.
        """
        vision_url = f"{self.endpoint}vision/v3.2/read/analyze"
        headers = {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/octet-stream'
        }

        # Initial request
        if not image_data:
            raise ValueError("Image data cannot be empty")

        response = requests.post(
            vision_url,
            headers=headers,
            data=image_data,
            timeout=REQUEST_TIMEOUT
        )
        if response.status_code != 202:
            raise Exception(f"Request failed with status {response.status_code}")

        # Get operation URL
        operation_url = response.headers.get("Operation-Location")
        if not operation_url:
            raise Exception("Azure response did not include an operation URL")
        if urlparse(operation_url).scheme != "https":
            raise Exception("Azure returned an invalid operation URL")

        # Poll for results
        deadline = time.monotonic() + POLL_TIMEOUT_SECONDS
        while True:
            if time.monotonic() >= deadline:
                raise TimeoutError("Azure OCR operation timed out")
            time.sleep(POLL_INTERVAL_SECONDS)
            response = requests.get(operation_url, headers={
                'Ocp-Apim-Subscription-Key': self.api_key
            }, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            result = response.json()

            if result.get("status") not in ["notStarted", "running"]:
                break

        if result.get("status") == "succeeded":
            text_results = []
            for read_result in result.get("analyzeResult", {}).get("readResults", []):
                for line in read_result.get("lines", []):
                    text_results.append(line.get("text", ""))
            return "\n".join(text_results)
        else:
            raise Exception("Failed to process the image")


class OpenAIService:
    def __init__(self, api_key: str):
        api_key = api_key.strip()
        if not api_key:
            raise ValueError("OpenAI API key is required")

        http_client = httpx.Client(
            base_url="https://api.openai.com/v1",
            follow_redirects=True,
            timeout=httpx.Timeout(60.0, connect=10.0)
        )
        self.client = OpenAI(
            api_key=api_key,
            http_client=http_client
        )

    def get_response(self, question: str, response_format: str = "Full Response") -> str:
        """
        Determines the question type and generates a response using GPT-4.
        """
        question = question.strip()
        if not question:
            raise ValueError("Question cannot be empty")

        try:
            # Detect question type
            question_type_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert at classifying interview questions. Respond with only 'technical' or 'behavioral'."},
                    {"role": "user", "content": f"Is this a technical or behavioral interview question? Question: {question}"}
                ]
            )

            question_type = question_type_response.choices[0].message.content.lower()
            is_full_response = response_format == "Full Response"

            # Prepare system prompt
            if "technical" in question_type:
                if is_full_response:
                    system_prompt = """You are an expert technical interview coach helping a candidate prepare for interviews. Provide a clear, concise, and technically accurate model answer that the candidate can study and learn from.
                    Include code examples if relevant. Format your response in a structured way:
                    1. Direct Answer
                    2. Technical Explanation
                    3. Example (with code if applicable)
                    4. Best Practices/Tips
                    Your goal is to teach the candidate how to think about and structure their own answer."""
                else:
                    system_prompt = """You are an expert technical interview coach helping a candidate prepare. Provide a concise model answer to the technical question that highlights the key points a strong candidate should cover."""
            else:
                if is_full_response:
                    system_prompt = """You are an expert behavioral interview coach helping a candidate prepare. Provide a model answer using the STAR method so the candidate can study the structure and craft their own authentic response:
                    1. Situation: Set up a relevant example
                    2. Task: What was required
                    3. Action: What you did
                    4. Result: The outcome
                    Encourage the candidate to adapt this framework to their own real experiences."""
                else:
                    system_prompt = """You are an expert behavioral interview coach helping a candidate prepare. Provide a brief model answer highlighting the key points to cover, so the candidate can use it as a reference when forming their own authentic response."""

            # Get GPT-4 response
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": question}
                ]
            )

            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response: {str(e)}")
