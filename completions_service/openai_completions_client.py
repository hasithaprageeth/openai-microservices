import openai
from completions_service import config
from completions_service.completion_response import CompletionResponse
from completions_service.models import Completion

openai.api_key = config.OPENAI_API_KEY.replace("\r\n", "")
model_engine = config.MODEL_ENGINE


def get_completion_response(prompt: str, session):
    """
        Sends a request to the OpenAI Chat API and returns the completion response.
    """
    response = openai.Completion.create(
        model=model_engine,
        prompt=prompt
    )

    # Generate completion model
    completion = __generate_completion_model(prompt, response)

    # Save completion to database
    session.add(completion)
    session.commit()

    # Return completion response
    return __prepare_completion_response(completion)


def __generate_completion_model(prompt: str, response):
    completed_text = response.choices[0].text.strip()
    return Completion(prompt, completed_text)


def __prepare_completion_response(completion: Completion):
    return CompletionResponse(completion.prompt, completion.completed_text)
