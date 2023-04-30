import openai
from edit_service import config
from edit_service.edit_response import EditResponse
from edit_service.models import Edit

openai.api_key = config.OPENAI_API_KEY.replace("\r\n", "")
model_engine = config.MODEL_ENGINE


def get_edit_response(instruction: str, prompt: str, session):
    """
        Sends a request to the OpenAI Chat API and returns the edit response.
    """
    response = openai.Edit.create(
        model=model_engine,
        instruction=instruction,
        input=prompt
    )

    # Generate edit model
    edit = __generate_edit_model(instruction, prompt, response)

    # Save chat to database
    session.add(edit)
    session.commit()

    # Return edit response
    return __prepare_edit_response(edit)


def __generate_edit_model(instruction: str, prompt: str, response):
    edited_text = response.choices[0].text.strip()
    return Edit(instruction, prompt, edited_text)


def __prepare_edit_response(edit: Edit):
    return EditResponse(edit.prompt, edit.edited_text)

