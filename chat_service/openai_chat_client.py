import openai
from chat_service import config
from chat_service.chat_response import ChatResponse
from chat_service.models import Chat

openai.api_key = config.OPENAI_API_KEY.replace("\r\n", "")
model_engine = config.MODEL_ENGINE


def get_chat_response(role: str, prompt: str, session):
    """
        Sends a request to the OpenAI Chat API and returns the chat response.
    """
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": role, "content": prompt},
        ]
    )

    # Generate chat model
    chat = __generate_chat_model(role, prompt, response)

    # Save chat to database
    session.add(chat)
    session.commit()

    # Return chat response
    return __prepare_chat_response(chat)


def __generate_chat_model(role: str, prompt: str, response):
    openai_message = response.choices[0].message
    return Chat(role, prompt, openai_message.get("role"), openai_message.get("content").strip())


def __prepare_chat_response(chat: Chat):
    return ChatResponse(chat.response_role, chat.response)
