import requests
import time
from openai import OpenAI
import httpx

class AzureOCRService:
    def __init__(self, endpoint: str, api_key: str):
        self.endpoint = endpoint
        self.api_key = api_key

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
        response = requests.post(vision_url, headers=headers, data=image_data)
        if response.status_code != 202:
            raise Exception(f"Request failed with status {response.status_code}")

        # Get operation URL
        operation_url = response.headers["Operation-Location"]

        # Poll for results
        while True:
            time.sleep(1)
            response = requests.get(operation_url, headers={
                'Ocp-Apim-Subscription-Key': self.api_key
            })
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
        http_client = httpx.Client(
            base_url="https://api.openai.com/v1",
            follow_redirects=True
        )
        self.client = OpenAI(
            api_key=api_key,
            http_client=http_client
        )

    def get_response(self, question: str, response_format: str = "Full Response") -> str:
        """
        Determines the question type and generates a response using GPT-4.
        """
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
                    system_prompt = """You are an expert technical interviewer. Provide a clear, concise, and technically accurate response to the interview question.
                    Include code examples if relevant. Format your response in a structured way:
                    1. Direct Answer
                    2. Technical Explanation
                    3. Example (with code if applicable)
                    4. Best Practices/Tips"""
                else:
                    system_prompt = """You are an expert technical interviewer. Provide only a direct, concise answer to the technical question without additional explanation or examples."""
            else:
                if is_full_response:
                    system_prompt = """You are an expert behavioral interviewer. Provide a response using the STAR method:
                    1. Situation: Set up a relevant example
                    2. Task: What was required
                    3. Action: What you did
                    4. Result: The outcome
                    Make the response personal and authentic while highlighting key soft skills."""
                else:
                    system_prompt = """You are an expert behavioral interviewer. Provide a brief, direct answer focusing only on the key points, without using the STAR method or detailed examples."""

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
