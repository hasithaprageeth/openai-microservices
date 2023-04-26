import os
import openai
from edit_models.edit_response import EditResponse

openai.api_key = os.environ['OPENAI_API_KEY']
model_engine = "text-davinci-edit-001"


def get_edit_response(instruction: str, prompt: str):
    """
        Sends a request to the OpenAI Chat API and returns the edit response.
    """
    response = openai.Edit.create(
        model=model_engine,
        instruction=instruction,
        input=prompt
    )
    edited_text = response.choices[0].text.strip()
    return __prepare_edit_response(prompt, edited_text)


def __prepare_edit_response(prompt: str, edited_text: str):
    response = EditResponse(prompt, edited_text)
    return response.__dict__
