import os
import openai
from completion_models.completion_response import CompletionResponse

openai.api_key = os.environ['OPENAI_API_KEY']
model_engine = "text-davinci-003"


def get_completion_response(prompt: str):
    """
        Sends a request to the OpenAI Chat API and returns the completion response.
    """
    response = openai.Completion.create(
        model=model_engine,
        prompt=prompt
    )
    completed_text = response.choices[0].text.strip()
    return __prepare_complete_response(prompt, completed_text)


def __prepare_complete_response(prompt: str, completed_text: str):
    response = CompletionResponse(prompt, completed_text)
    return response.__dict__
